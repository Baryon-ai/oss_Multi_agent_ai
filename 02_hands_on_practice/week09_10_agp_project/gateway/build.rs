fn main() -> Result<(), Box<dyn std::error::Error>> {
    // gRPC proto 파일 컴파일
    tonic_build::compile_protos("proto/agp.proto")?;
    tonic_build::compile_protos("proto/health.proto")?;
    Ok(())
} 