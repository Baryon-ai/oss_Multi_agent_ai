#!/usr/bin/env python3
"""
AGP Workflow Example - Machine Learning Pipeline
Demonstrates how to orchestrate ML workflow using AGP protocol
"""

import asyncio
import grpc
import json
import logging
from typing import Dict, Any, List
from datetime import datetime
import uuid

# Generated gRPC client (would be generated from proto file)
# import agp_pb2
# import agp_pb2_grpc

# Mock implementation for demonstration
class MockAGPClient:
    """Mock AGP client for demonstration purposes"""
    
    def __init__(self, gateway_url: str = "localhost:50051"):
        self.gateway_url = gateway_url
        self.logger = logging.getLogger(__name__)
    
    async def send_message(self, agent_id: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send message to agent via AGP gateway"""
        self.logger.info(f"Sending message to {agent_id}: {message['type']}")
        
        # Simulate processing time
        await asyncio.sleep(1.0)
        
        # Mock responses based on agent type
        if "data_analyst" in agent_id:
            return {
                "status": "completed",
                "result": {
                    "data_shape": [1000, 50],
                    "missing_values": 23,
                    "outliers_detected": 7,
                    "processed_data_path": "/tmp/processed_data.csv"
                },
                "metadata": {
                    "processing_time": 2.3,
                    "memory_usage": "125MB"
                }
            }
        elif "ml_trainer" in agent_id:
            return {
                "status": "completed", 
                "result": {
                    "model_accuracy": 0.94,
                    "model_path": "/tmp/trained_model.pkl",
                    "training_loss": 0.156,
                    "validation_loss": 0.203,
                    "epochs": 50
                },
                "metadata": {
                    "training_time": 45.7,
                    "gpu_utilization": "87%"
                }
            }
        elif "inference_service" in agent_id:
            return {
                "status": "completed",
                "result": {
                    "predictions": [0.85, 0.92, 0.78, 0.91],
                    "confidence_scores": [0.94, 0.87, 0.82, 0.96],
                    "prediction_time": 0.023
                },
                "metadata": {
                    "model_version": "v1.2.3",
                    "inference_engine": "AGP-optimized"
                }
            }
        else:
            return {"status": "error", "message": f"Unknown agent: {agent_id}"}
    
    async def publish_event(self, topic: str, event: Dict[str, Any]) -> bool:
        """Publish event to AGP pub/sub system"""
        self.logger.info(f"Publishing event to {topic}: {event['type']}")
        await asyncio.sleep(0.1)
        return True
    
    async def subscribe_events(self, topic: str):
        """Subscribe to events from AGP pub/sub system"""
        self.logger.info(f"Subscribing to events on topic: {topic}")
        
        # Mock event stream
        events = [
            {"type": "workflow_started", "workflow_id": "ml_pipeline_001"},
            {"type": "data_processing_complete", "stage": "preprocessing"},
            {"type": "model_training_started", "stage": "training"},
            {"type": "model_training_complete", "stage": "training"},
            {"type": "inference_ready", "stage": "deployment"},
            {"type": "workflow_complete", "workflow_id": "ml_pipeline_001"}
        ]
        
        for event in events:
            await asyncio.sleep(2.0)
            yield event

class MLWorkflowOrchestrator:
    """Machine Learning Workflow Orchestrator using AGP"""
    
    def __init__(self, agp_client: MockAGPClient):
        self.agp_client = agp_client
        self.logger = logging.getLogger(__name__)
        self.workflow_id = str(uuid.uuid4())
        
    async def execute_ml_pipeline(self, dataset_path: str, target_column: str) -> Dict[str, Any]:
        """Execute complete ML pipeline using AGP agents"""
        
        self.logger.info(f"Starting ML pipeline {self.workflow_id}")
        
        pipeline_config = {
            "workflow_id": self.workflow_id,
            "dataset_path": dataset_path,
            "target_column": target_column,
            "stages": ["data_processing", "model_training", "model_evaluation", "inference_setup"],
            "agents": {
                "data_analyst": "agp://data_analyst_agent",
                "ml_trainer": "agp://ml_trainer_agent", 
                "inference_service": "agp://inference_agent"
            }
        }
        
        results = {}
        
        try:
            # Stage 1: Data Processing
            self.logger.info("Stage 1: Data Processing")
            await self.agp_client.publish_event("ml_pipeline", {
                "type": "stage_started",
                "stage": "data_processing",
                "workflow_id": self.workflow_id
            })
            
            data_processing_result = await self.agp_client.send_message(
                "data_analyst_agent",
                {
                    "type": "process_data",
                    "workflow_id": self.workflow_id,
                    "parameters": {
                        "dataset_path": dataset_path,
                        "target_column": target_column,
                        "preprocessing_steps": ["clean", "normalize", "feature_engineering"]
                    }
                }
            )
            
            if data_processing_result["status"] != "completed":
                raise Exception(f"Data processing failed: {data_processing_result}")
            
            results["data_processing"] = data_processing_result
            processed_data_path = data_processing_result["result"]["processed_data_path"]
            
            # Stage 2: Model Training
            self.logger.info("Stage 2: Model Training")
            await self.agp_client.publish_event("ml_pipeline", {
                "type": "stage_started",
                "stage": "model_training",
                "workflow_id": self.workflow_id
            })
            
            training_result = await self.agp_client.send_message(
                "ml_trainer_agent",
                {
                    "type": "train_model",
                    "workflow_id": self.workflow_id,
                    "parameters": {
                        "processed_data_path": processed_data_path,
                        "model_type": "random_forest",
                        "hyperparameters": {
                            "n_estimators": 100,
                            "max_depth": 10,
                            "random_state": 42
                        }
                    }
                }
            )
            
            if training_result["status"] != "completed":
                raise Exception(f"Model training failed: {training_result}")
            
            results["model_training"] = training_result
            model_path = training_result["result"]["model_path"]
            
            # Stage 3: Model Evaluation
            self.logger.info("Stage 3: Model Evaluation")
            evaluation_result = await self.agp_client.send_message(
                "ml_trainer_agent",
                {
                    "type": "evaluate_model",
                    "workflow_id": self.workflow_id,
                    "parameters": {
                        "model_path": model_path,
                        "test_data_path": processed_data_path,
                        "metrics": ["accuracy", "precision", "recall", "f1_score"]
                    }
                }
            )
            
            results["model_evaluation"] = evaluation_result
            
            # Stage 4: Inference Service Setup
            self.logger.info("Stage 4: Inference Service Setup")
            inference_setup_result = await self.agp_client.send_message(
                "inference_agent",
                {
                    "type": "deploy_model",
                    "workflow_id": self.workflow_id,
                    "parameters": {
                        "model_path": model_path,
                        "endpoint_config": {
                            "max_batch_size": 32,
                            "timeout": 30,
                            "auto_scaling": True
                        }
                    }
                }
            )
            
            results["inference_setup"] = inference_setup_result
            
            # Test inference
            self.logger.info("Testing inference")
            test_prediction = await self.agp_client.send_message(
                "inference_agent",
                {
                    "type": "predict",
                    "workflow_id": self.workflow_id,
                    "parameters": {
                        "input_data": [[1.2, 3.4, 5.6, 7.8]],  # Sample input
                        "return_confidence": True
                    }
                }
            )
            
            results["test_prediction"] = test_prediction
            
            # Pipeline completion
            await self.agp_client.publish_event("ml_pipeline", {
                "type": "workflow_complete",
                "workflow_id": self.workflow_id,
                "status": "success",
                "duration": 120.5,  # Mock duration
                "stages_completed": 4
            })
            
            self.logger.info(f"ML pipeline {self.workflow_id} completed successfully")
            
            return {
                "workflow_id": self.workflow_id,
                "status": "completed",
                "results": results,
                "summary": {
                    "data_points_processed": data_processing_result["result"]["data_shape"][0],
                    "model_accuracy": training_result["result"]["model_accuracy"],
                    "inference_ready": True,
                    "total_pipeline_time": sum([
                        results["data_processing"]["metadata"]["processing_time"],
                        results["model_training"]["metadata"]["training_time"]
                    ])
                }
            }
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            
            await self.agp_client.publish_event("ml_pipeline", {
                "type": "workflow_failed",
                "workflow_id": self.workflow_id,
                "error": str(e)
            })
            
            return {
                "workflow_id": self.workflow_id,
                "status": "failed",
                "error": str(e),
                "partial_results": results
            }

async def monitor_pipeline_events(agp_client: MockAGPClient):
    """Monitor pipeline events in real-time"""
    logger = logging.getLogger(__name__)
    
    logger.info("Starting pipeline event monitoring...")
    
    async for event in agp_client.subscribe_events("ml_pipeline"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        logger.info(f"[{timestamp}] Pipeline Event: {event['type']}")
        
        if event.get("type") == "workflow_complete":
            logger.info("Pipeline monitoring complete")
            break

async def main():
    """Main example execution"""
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting AGP ML Workflow Example")
    
    # Initialize AGP client
    agp_client = MockAGPClient("localhost:50051")
    
    # Create workflow orchestrator
    orchestrator = MLWorkflowOrchestrator(agp_client)
    
    # Start event monitoring in background
    monitor_task = asyncio.create_task(monitor_pipeline_events(agp_client))
    
    # Execute ML pipeline
    pipeline_result = await orchestrator.execute_ml_pipeline(
        dataset_path="/data/customer_churn.csv",
        target_column="churn"
    )
    
    # Wait for monitoring to complete
    await monitor_task
    
    # Print results
    logger.info("=" * 60)
    logger.info("ML Pipeline Results Summary")
    logger.info("=" * 60)
    
    if pipeline_result["status"] == "completed":
        summary = pipeline_result["summary"]
        logger.info(f"Workflow ID: {pipeline_result['workflow_id']}")
        logger.info(f"Data Points Processed: {summary['data_points_processed']:,}")
        logger.info(f"Model Accuracy: {summary['model_accuracy']:.2%}")
        logger.info(f"Total Pipeline Time: {summary['total_pipeline_time']:.1f}s")
        logger.info(f"Inference Ready: {summary['inference_ready']}")
        
        # Show detailed results
        for stage, result in pipeline_result["results"].items():
            logger.info(f"\n{stage.upper()}:")
            if "result" in result:
                for key, value in result["result"].items():
                    logger.info(f"  {key}: {value}")
    else:
        logger.error(f"Pipeline failed: {pipeline_result.get('error', 'Unknown error')}")
    
    logger.info("\nAGP ML Workflow Example completed")

if __name__ == "__main__":
    asyncio.run(main()) 