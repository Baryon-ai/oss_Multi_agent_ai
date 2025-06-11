pub mod agp_service {
    use tonic::{Request, Response, Status};
    use crate::agp::{MessageRequest, MessageResponse};
    use crate::agp::agp_gateway_server::AgpGateway;
    
    #[derive(Debug, Default)]
    pub struct AgpGatewayService {}
    
    #[tonic::async_trait]
    impl AgpGateway for AgpGatewayService {
        async fn send_message(
            &self,
            request: Request<MessageRequest>,
        ) -> Result<Response<MessageResponse>, Status> {
            let req = request.into_inner();
            let response = MessageResponse {
                message_id: req.message_id,
                status: "delivered".to_string(),
                metadata: req.metadata,
            };
            
            Ok(Response::new(response))
        }
        
        async fn get_health(
            &self,
            _request: Request<crate::agp::HealthRequest>,
        ) -> Result<Response<crate::agp::HealthResponse>, Status> {
            let response = crate::agp::HealthResponse {
                status: "healthy".to_string(),
            };
            Ok(Response::new(response))
        }
    }
}

pub use agp_service::AgpGatewayService; 