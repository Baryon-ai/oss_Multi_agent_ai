// AGP Gateway - Main Entry Point
// High-performance agent gateway using gRPC and Rust

use std::net::SocketAddr;
use tonic::{transport::Server, Request, Response, Status};
use tokio::signal;
use tracing::{info, error};

mod gateway;
mod router;
mod auth;

use gateway::AgpGatewayService;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize tracing for observability
    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::INFO)
        .init();

    info!("Starting AGP Gateway...");

    // Gateway configuration
    let config = GatewayConfig::from_env();
    let addr: SocketAddr = config.listen_addr.parse()?;

    // Create gateway service
    let gateway_service = AgpGatewayService::default();

    info!("AGP Gateway listening on {}", addr);

    // Build gRPC server
    let server = Server::builder()
        .add_service(AgpGatewayServer::new(gateway_service))
        .serve_with_shutdown(addr, shutdown_signal());

    // Start server
    if let Err(e) = server.await {
        error!("Server error: {}", e);
    }

    info!("AGP Gateway shutting down...");
    Ok(())
}

async fn shutdown_signal() {
    let ctrl_c = async {
        signal::ctrl_c()
            .await
            .expect("failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {
            info!("Received Ctrl+C signal");
        }
        _ = terminate => {
            info!("Received SIGTERM signal");
        }
    }
}

#[derive(Clone)]
pub struct GatewayConfig {
    pub listen_addr: String,
    pub redis_url: String,
    pub postgres_url: String,
    pub tls_cert_path: String,
    pub tls_key_path: String,
    pub enable_mtls: bool,
    pub oauth2_endpoint: String,
}

impl GatewayConfig {
    pub fn from_env() -> Self {
        Self {
            listen_addr: std::env::var("GATEWAY_LISTEN_ADDR")
                .unwrap_or_else(|_| "[::1]:50051".to_string()),
            redis_url: std::env::var("REDIS_URL")
                .unwrap_or_else(|_| "redis://localhost:6379".to_string()),
            postgres_url: std::env::var("DATABASE_URL")
                .unwrap_or_else(|_| "postgresql://localhost:5432/agp".to_string()),
            tls_cert_path: std::env::var("TLS_CERT_PATH")
                .unwrap_or_else(|_| "./configs/tls/server.crt".to_string()),
            tls_key_path: std::env::var("TLS_KEY_PATH")
                .unwrap_or_else(|_| "./configs/tls/server.key".to_string()),
            enable_mtls: std::env::var("ENABLE_MTLS")
                .unwrap_or_else(|_| "false".to_string())
                .parse()
                .unwrap_or(false),
            oauth2_endpoint: std::env::var("OAUTH2_ENDPOINT")
                .unwrap_or_else(|_| "http://localhost:8080/auth".to_string()),
        }
    }
}

// Health check endpoint for Kubernetes/Docker
#[derive(Default)]
pub struct HealthService;

#[tonic::async_trait]
impl health::health_server::Health for HealthService {
    async fn check(
        &self,
        _request: Request<health::HealthCheckRequest>,
    ) -> Result<Response<health::HealthCheckResponse>, Status> {
        Ok(Response::new(health::HealthCheckResponse {
            status: health::health_check_response::ServingStatus::Serving as i32,
        }))
    }

    type WatchStream = tokio_stream::wrappers::ReceiverStream<Result<health::HealthCheckResponse, Status>>;

    async fn watch(
        &self,
        _request: Request<health::HealthCheckRequest>,
    ) -> Result<Response<Self::WatchStream>, Status> {
        Err(Status::unimplemented("Health watch not implemented"))
    }
}

// Include generated proto modules
pub mod agp {
    tonic::include_proto!("agp");
}

pub mod health {
    tonic::include_proto!("grpc.health.v1");
}

use agp::agp_gateway_server::{AgpGateway, AgpGatewayServer};
use health::health_server::{Health, HealthServer};

// Performance metrics collection (placeholder)
#[derive(Clone)]
pub struct Metrics {
    pub requests_total: u64,
    pub active_connections: u64,
}

impl Metrics {
    pub fn new() -> Self {
        Self {
            requests_total: 0,
            active_connections: 0,
        }
    }
} 