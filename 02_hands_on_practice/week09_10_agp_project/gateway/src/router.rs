use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct Router {
    routes: HashMap<String, String>,
}

impl Router {
    pub fn new() -> Self {
        Self {
            routes: HashMap::new(),
        }
    }
    
    pub fn add_route(&mut self, agent_id: String, endpoint: String) {
        self.routes.insert(agent_id, endpoint);
    }
    
    pub fn get_route(&self, agent_id: &str) -> Option<&String> {
        self.routes.get(agent_id)
    }
}

impl Default for Router {
    fn default() -> Self {
        Self::new()
    }
} 