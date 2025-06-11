#!/bin/bash
# ACP Federation Platform - cURL Examples
# Demonstrates how to interact with ACP agents using pure REST API calls

set -e

# Configuration
ACP_BASE_URL="http://localhost:8000"
AGENT_ID="langchain_qa"
CONTENT_TYPE="application/json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if platform is running
check_platform() {
    print_header "Checking ACP Federation Platform"
    
    response=$(curl -s -w "%{http_code}" -o /tmp/platform_status "$ACP_BASE_URL/" || echo "000")
    
    if [ "$response" -eq 200 ]; then
        print_success "Platform is running"
        cat /tmp/platform_status | jq '.'
    else
        print_error "Platform is not running (HTTP $response)"
        echo "Please start the platform with: python federation_platform/main.py"
        exit 1
    fi
}

# List all available agents
list_agents() {
    print_header "Listing Available Agents"
    
    curl -s -X GET \
        -H "Content-Type: $CONTENT_TYPE" \
        "$ACP_BASE_URL/discovery/agents" | jq '.'
}

# Get agent details
get_agent_details() {
    local agent_id=${1:-$AGENT_ID}
    
    print_header "Getting Agent Details: $agent_id"
    
    response=$(curl -s -w "%{http_code}" -o /tmp/agent_details \
        -X GET \
        -H "Content-Type: $CONTENT_TYPE" \
        "$ACP_BASE_URL/agents/$agent_id")
    
    if [ "$response" -eq 200 ]; then
        print_success "Agent details retrieved"
        cat /tmp/agent_details | jq '.'
    else
        print_error "Failed to get agent details (HTTP $response)"
        cat /tmp/agent_details
    fi
}

# Simple Q&A example
simple_qa_example() {
    print_header "Simple Q&A Example"
    
    local question="What is the capital of France?"
    
    print_info "Sending question: $question"
    
    # Create the run
    run_response=$(curl -s -w "%{http_code}" -o /tmp/run_create \
        -X POST \
        -H "Content-Type: $CONTENT_TYPE" \
        -d '{
            "input": [
                {
                    "parts": [
                        {
                            "content": "'"$question"'",
                            "content_type": "text/plain"
                        }
                    ]
                }
            ]
        }' \
        "$ACP_BASE_URL/agents/$AGENT_ID/runs")
    
    if [ "$run_response" -eq 200 ]; then
        print_success "Run created successfully"
        run_id=$(cat /tmp/run_create | jq -r '.run_id')
        print_info "Run ID: $run_id"
        
        # Poll for results
        print_info "Waiting for results..."
        sleep 3
        
        # Get run status and results
        result_response=$(curl -s -w "%{http_code}" -o /tmp/run_result \
            -X GET \
            -H "Content-Type: $CONTENT_TYPE" \
            "$ACP_BASE_URL/agents/$AGENT_ID/runs/$run_id")
        
        if [ "$result_response" -eq 200 ]; then
            print_success "Results retrieved"
            cat /tmp/run_result | jq '.'
        else
            print_error "Failed to get results (HTTP $result_response)"
            cat /tmp/run_result
        fi
    else
        print_error "Failed to create run (HTTP $run_response)"
        cat /tmp/run_create
    fi
}

# Code generation example
code_generation_example() {
    print_header "Code Generation Example"
    
    local request="Write a Python function to calculate the factorial of a number"
    
    print_info "Sending request: $request"
    
    # Create the run for coding agent
    run_response=$(curl -s -w "%{http_code}" -o /tmp/code_run_create \
        -X POST \
        -H "Content-Type: $CONTENT_TYPE" \
        -d '{
            "input": [
                {
                    "parts": [
                        {
                            "content": "'"$request"'",
                            "content_type": "text/plain"
                        }
                    ]
                }
            ]
        }' \
        "$ACP_BASE_URL/agents/autogen_coder/runs")
    
    if [ "$run_response" -eq 200 ]; then
        print_success "Code generation run created"
        run_id=$(cat /tmp/code_run_create | jq -r '.run_id')
        print_info "Run ID: $run_id"
        
        # Wait for processing
        sleep 5
        
        # Get results
        curl -s -X GET \
            -H "Content-Type: $CONTENT_TYPE" \
            "$ACP_BASE_URL/agents/autogen_coder/runs/$run_id" | jq '.'
    else
        print_error "Failed to create code generation run"
        cat /tmp/code_run_create
    fi
}

# Data analysis example
data_analysis_example() {
    print_header "Data Analysis Example"
    
    local data_request="Analyze this dataset and provide insights"
    local sample_data='[{"name": "Alice", "age": 30, "salary": 70000}, {"name": "Bob", "age": 25, "salary": 60000}, {"name": "Charlie", "age": 35, "salary": 80000}]'
    
    print_info "Sending data analysis request"
    
    # Create analysis run
    run_response=$(curl -s -w "%{http_code}" -o /tmp/analysis_run_create \
        -X POST \
        -H "Content-Type: $CONTENT_TYPE" \
        -d '{
            "input": [
                {
                    "parts": [
                        {
                            "content": "'"$data_request"'",
                            "content_type": "text/plain"
                        },
                        {
                            "content": '"$(echo "$sample_data" | jq -c .)"',
                            "content_type": "application/json"
                        }
                    ]
                }
            ]
        }' \
        "$ACP_BASE_URL/agents/custom_analyzer/runs")
    
    if [ "$run_response" -eq 200 ]; then
        print_success "Data analysis run created"
        run_id=$(cat /tmp/analysis_run_create | jq -r '.run_id')
        
        # Wait for processing
        sleep 4
        
        # Get results
        curl -s -X GET \
            -H "Content-Type: $CONTENT_TYPE" \
            "$ACP_BASE_URL/agents/custom_analyzer/runs/$run_id" | jq '.'
    else
        print_error "Failed to create data analysis run"
        cat /tmp/analysis_run_create
    fi
}

# Multi-agent collaboration example
collaboration_example() {
    print_header "Multi-Agent Collaboration Example"
    
    print_info "Starting collaborative task: Write and analyze a Python script"
    
    # Step 1: Generate code
    print_info "Step 1: Generating code with AutoGen agent"
    
    code_request="Write a Python function to calculate prime numbers up to n using the Sieve of Eratosthenes algorithm"
    
    code_run=$(curl -s -X POST \
        -H "Content-Type: $CONTENT_TYPE" \
        -d '{
            "input": [
                {
                    "parts": [
                        {
                            "content": "'"$code_request"'",
                            "content_type": "text/plain"
                        }
                    ]
                }
            ]
        }' \
        "$ACP_BASE_URL/agents/autogen_coder/runs")
    
    code_run_id=$(echo "$code_run" | jq -r '.run_id')
    print_info "Code generation run ID: $code_run_id"
    
    # Wait for code generation
    sleep 5
    
    # Get generated code
    code_result=$(curl -s -X GET \
        -H "Content-Type: $CONTENT_TYPE" \
        "$ACP_BASE_URL/agents/autogen_coder/runs/$code_run_id")
    
    generated_code=$(echo "$code_result" | jq -r '.output[0].parts[0].content // "No code generated"')
    
    if [ "$generated_code" != "No code generated" ]; then
        print_success "Code generated successfully"
        
        # Step 2: Analyze the code
        print_info "Step 2: Analyzing code with Custom analyzer"
        
        analysis_request="Analyze this Python code for performance, readability, and best practices"
        
        analysis_run=$(curl -s -X POST \
            -H "Content-Type: $CONTENT_TYPE" \
            -d '{
                "input": [
                    {
                        "parts": [
                            {
                                "content": "'"$analysis_request"'",
                                "content_type": "text/plain"
                            },
                            {
                                "content": "'"$(echo "$generated_code" | sed 's/"/\\"/g' | tr -d '\n')"'",
                                "content_type": "text/plain"
                            }
                        ]
                    }
                ]
            }' \
            "$ACP_BASE_URL/agents/custom_analyzer/runs")
        
        analysis_run_id=$(echo "$analysis_run" | jq -r '.run_id')
        print_info "Code analysis run ID: $analysis_run_id"
        
        # Wait for analysis
        sleep 4
        
        # Get analysis results
        curl -s -X GET \
            -H "Content-Type: $CONTENT_TYPE" \
            "$ACP_BASE_URL/agents/custom_analyzer/runs/$analysis_run_id" | jq '.'
        
        print_success "Multi-agent collaboration completed"
    else
        print_error "Code generation failed, skipping analysis step"
    fi
}

# Streaming example (using Server-Sent Events)
streaming_example() {
    print_header "Streaming Example"
    
    print_info "Creating a long-running task to demonstrate streaming"
    
    # Create a run that will stream results
    run_response=$(curl -s -X POST \
        -H "Content-Type: $CONTENT_TYPE" \
        -d '{
            "input": [
                {
                    "parts": [
                        {
                            "content": "Explain the concept of machine learning in detail with examples",
                            "content_type": "text/plain"
                        }
                    ]
                }
            ]
        }' \
        "$ACP_BASE_URL/agents/$AGENT_ID/runs")
    
    run_id=$(echo "$run_response" | jq -r '.run_id')
    stream_url="$ACP_BASE_URL/agents/$AGENT_ID/runs/$run_id/stream"
    
    print_info "Streaming from: $stream_url"
    print_info "Listening for 10 seconds..."
    
    # Listen to the stream for 10 seconds
    timeout 10s curl -s -N \
        -H "Accept: text/event-stream" \
        -H "Cache-Control: no-cache" \
        "$stream_url" | while IFS= read -r line; do
        
        if [[ $line == data:* ]]; then
            # Extract JSON data and pretty print
            json_data=${line#data: }
            echo "$json_data" | jq '.' 2>/dev/null || echo "$line"
        fi
    done || print_info "Stream timeout reached"
}

# Federation learning example
federation_example() {
    print_header "Federation Learning Example"
    
    print_info "Demonstrating federated learning capabilities"
    
    # Create a federation task
    federation_request='{
        "federation_name": "qa_knowledge_sharing",
        "participants": ["langchain_qa", "autogen_coder", "custom_analyzer"],
        "task": {
            "type": "knowledge_aggregation",
            "input": [
                {
                    "parts": [
                        {
                            "content": "What are the best practices for writing maintainable code?",
                            "content_type": "text/plain"
                        }
                    ]
                }
            ]
        },
        "aggregation_method": "consensus"
    }'
    
    curl -s -X POST \
        -H "Content-Type: $CONTENT_TYPE" \
        -d "$federation_request" \
        "$ACP_BASE_URL/federation/tasks" | jq '.'
}

# Health check
health_check() {
    print_header "Platform Health Check"
    
    curl -s -X GET \
        -H "Content-Type: $CONTENT_TYPE" \
        "$ACP_BASE_URL/health" | jq '.'
}

# Platform metrics
platform_metrics() {
    print_header "Platform Metrics"
    
    curl -s -X GET \
        -H "Content-Type: $CONTENT_TYPE" \
        "$ACP_BASE_URL/metrics" | jq '.'
}

# Main execution
main() {
    echo -e "${BLUE}"
    echo "=========================================="
    echo "  ACP Federation Platform - cURL Examples"
    echo "=========================================="
    echo -e "${NC}"
    
    # Check if jq is installed
    if ! command -v jq &> /dev/null; then
        print_error "jq is required for JSON parsing. Please install it first."
        exit 1
    fi
    
    # Parse command line arguments
    case "${1:-all}" in
        "check")
            check_platform
            ;;
        "agents")
            check_platform
            list_agents
            ;;
        "details")
            check_platform
            get_agent_details "${2:-$AGENT_ID}"
            ;;
        "qa")
            check_platform
            simple_qa_example
            ;;
        "code")
            check_platform
            code_generation_example
            ;;
        "analysis")
            check_platform
            data_analysis_example
            ;;
        "collab")
            check_platform
            collaboration_example
            ;;
        "stream")
            check_platform
            streaming_example
            ;;
        "federation")
            check_platform
            federation_example
            ;;
        "health")
            health_check
            ;;
        "metrics")
            platform_metrics
            ;;
        "all")
            check_platform
            list_agents
            get_agent_details
            simple_qa_example
            code_generation_example
            data_analysis_example
            collaboration_example
            federation_example
            health_check
            platform_metrics
            ;;
        *)
            echo "Usage: $0 [check|agents|details|qa|code|analysis|collab|stream|federation|health|metrics|all]"
            echo ""
            echo "Examples:"
            echo "  $0 check         - Check if platform is running"
            echo "  $0 agents        - List all available agents"
            echo "  $0 details [id]  - Get agent details"
            echo "  $0 qa            - Simple Q&A example"
            echo "  $0 code          - Code generation example"
            echo "  $0 analysis      - Data analysis example"
            echo "  $0 collab        - Multi-agent collaboration"
            echo "  $0 stream        - Streaming results example"
            echo "  $0 federation    - Federation learning example"
            echo "  $0 health        - Platform health check"
            echo "  $0 metrics       - Platform metrics"
            echo "  $0 all           - Run all examples"
            exit 1
            ;;
    esac
}

# Cleanup temporary files on exit
cleanup() {
    rm -f /tmp/platform_status /tmp/agent_details /tmp/run_create /tmp/run_result
    rm -f /tmp/code_run_create /tmp/analysis_run_create
}
trap cleanup EXIT

# Run main function
main "$@" 