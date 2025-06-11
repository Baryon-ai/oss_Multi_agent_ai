use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct AuthManager {
    tokens: HashMap<String, String>,
}

impl AuthManager {
    pub fn new() -> Self {
        Self {
            tokens: HashMap::new(),
        }
    }
    
    pub fn add_token(&mut self, token: String, agent_id: String) {
        self.tokens.insert(token, agent_id);
    }
    
    pub fn verify_token(&self, token: &str) -> Option<&String> {
        self.tokens.get(token)
    }
}

impl Default for AuthManager {
    fn default() -> Self {
        Self::new()
    }
} 