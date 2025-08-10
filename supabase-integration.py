"""
Integração com Supabase para Investment Simulation System
Adiciona persistência de dados e autenticação
"""

import os
from typing import Optional, Dict, Any, List
from datetime import datetime
import json

try:
    from supabase import create_client, Client
except ImportError:
    print("⚠️  Supabase não instalado. Execute: pip install supabase")
    Client = None

class SupabaseIntegration:
    """Classe para integração com Supabase"""
    
    def __init__(self):
        self.supabase: Optional[Client] = None
        self.setup_client()
    
    def setup_client(self):
        """Configura cliente Supabase"""
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if url and key and Client:
            try:
                self.supabase = create_client(url, key)
                print("✅ Supabase conectado com sucesso")
            except Exception as e:
                print(f"❌ Erro ao conectar Supabase: {e}")
        else:
            print("⚠️  Variáveis de ambiente Supabase não configuradas")
    
    def is_connected(self) -> bool:
        """Verifica se está conectado ao Supabase"""
        return self.supabase is not None
    
    # Métodos para Usuários
    def create_user(self, email: str, name: str = None) -> Optional[Dict]:
        """Cria um novo usuário"""
        if not self.is_connected():
            return None
        
        try:
            result = self.supabase.table('users').insert({
                'email': email,
                'name': name,
                'created_at': datetime.utcnow().isoformat()
            }).execute()
            
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Busca usuário por email"""
        if not self.is_connected():
            return None
        
        try:
            result = self.supabase.table('users').select("*").eq('email', email).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None
    
    # Métodos para Simulações
    def save_simulation(self, user_id: str, strategy: str, parameters: Dict, result: Dict) -> Optional[Dict]:
        """Salva uma simulação no banco"""
        if not self.is_connected():
            return None
        
        try:
            simulation_data = {
                'user_id': user_id,
                'strategy': strategy,
                'parameters': json.dumps(parameters),
                'result': json.dumps(result),
                'created_at': datetime.utcnow().isoformat()
            }
            
            db_result = self.supabase.table('simulations').insert(simulation_data).execute()
            return db_result.data[0] if db_result.data else None
        except Exception as e:
            print(f"Erro ao salvar simulação: {e}")
            return None
    
    def get_user_simulations(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Busca simulações de um usuário"""
        if not self.is_connected():
            return []
        
        try:
            result = self.supabase.table('simulations')\
                .select("*")\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data or []
        except Exception as e:
            print(f"Erro ao buscar simulações: {e}")
            return []
    
    def get_simulation_stats(self) -> Dict[str, Any]:
        """Estatísticas gerais das simulações"""
        if not self.is_connected():
            return {}
        
        try:
            # Total de simulações
            total_result = self.supabase.table('simulations').select("id", count="exact").execute()
            total_simulations = total_result.count or 0
            
            # Simulações por estratégia
            strategy_result = self.supabase.rpc('get_strategy_stats').execute()
            strategy_stats = strategy_result.data or []
            
            return {
                'total_simulations': total_simulations,
                'strategy_distribution': strategy_stats,
                'last_updated': datetime.utcnow().isoformat()
            }
        except Exception as e:
            print(f"Erro ao buscar estatísticas: {e}")
            return {}
    
    # Métodos para Portfólios
    def save_portfolio(self, user_id: str, name: str, strategies: Dict, 
                      optimal_weights: Dict, final_return: float) -> Optional[Dict]:
        """Salva um portfólio otimizado"""
        if not self.is_connected():
            return None
        
        try:
            portfolio_data = {
                'user_id': user_id,
                'name': name,
                'strategies': json.dumps(strategies),
                'optimal_weights': json.dumps(optimal_weights),
                'final_return': final_return,
                'created_at': datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table('portfolios').insert(portfolio_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Erro ao salvar portfólio: {e}")
            return None
    
    def get_user_portfolios(self, user_id: str) -> List[Dict]:
        """Busca portfólios de um usuário"""
        if not self.is_connected():
            return []
        
        try:
            result = self.supabase.table('portfolios')\
                .select("*")\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .execute()
            
            return result.data or []
        except Exception as e:
            print(f"Erro ao buscar portfólios: {e}")
            return []

# Instância global
supabase_client = SupabaseIntegration()

# Funções de conveniência
def save_simulation_result(strategy: str, parameters: Dict, result: Dict, 
                         user_email: str = None) -> bool:
    """Salva resultado de simulação (função de conveniência)"""
    if not supabase_client.is_connected():
        return False
    
    # Se não tem email, cria usuário anônimo
    if not user_email:
        user_email = f"anonymous_{datetime.utcnow().timestamp()}"
    
    # Busca ou cria usuário
    user = supabase_client.get_user_by_email(user_email)
    if not user:
        user = supabase_client.create_user(user_email, "Usuário Anônimo")
    
    if not user:
        return False
    
    # Salva simulação
    simulation = supabase_client.save_simulation(
        user_id=user['id'],
        strategy=strategy,
        parameters=parameters,
        result=result
    )
    
    return simulation is not None

def get_simulation_history(user_email: str, limit: int = 10) -> List[Dict]:
    """Busca histórico de simulações de um usuário"""
    if not supabase_client.is_connected():
        return []
    
    user = supabase_client.get_user_by_email(user_email)
    if not user:
        return []
    
    return supabase_client.get_user_simulations(user['id'], limit)

# Exemplo de uso
if __name__ == "__main__":
    # Teste da integração
    print("🧪 Testando integração Supabase...")
    
    if supabase_client.is_connected():
        print("✅ Conectado ao Supabase")
        
        # Teste salvar simulação
        test_params = {
            "aporte_inicial": 100000,
            "aporte_mensal": 3000,
            "taxa_cdi": 10.5,
            "anos": 20
        }
        
        test_result = {
            "patrimonio_final": 1500000,
            "rentabilidade_total": 50.0,
            "rentabilidade_anual": 2.1
        }
        
        success = save_simulation_result(
            strategy="CDI",
            parameters=test_params,
            result=test_result,
            user_email="teste@exemplo.com"
        )
        
        if success:
            print("✅ Simulação salva com sucesso")
        else:
            print("❌ Erro ao salvar simulação")
        
        # Buscar histórico
        history = get_simulation_history("teste@exemplo.com")
        print(f"📊 Encontradas {len(history)} simulações no histórico")
        
    else:
        print("❌ Não conectado ao Supabase")
        print("Configure as variáveis de ambiente:")
        print("- SUPABASE_URL")
        print("- SUPABASE_ANON_KEY")