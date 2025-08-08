import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { 
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { 
  HelpCircle, 
  Search, 
  ChevronDown, 
  BookOpen, 
  Calculator,
  TrendingUp,
  Building,
  Target,
  Play,
  ExternalLink
} from "lucide-react";

interface FAQ {
  id: string;
  question: string;
  answer: string;
  category: string;
  tags: string[];
}

interface Tutorial {
  id: string;
  title: string;
  description: string;
  duration: string;
  level: 'Iniciante' | 'Intermediário' | 'Avançado';
  icon: any;
  steps: string[];
}

const faqs: FAQ[] = [
  {
    id: '1',
    question: 'Como calcular o rendimento da renda fixa?',
    answer: 'O rendimento da renda fixa é calculado com base na taxa de juros (CDI ou IPCA+), período de investimento e frequência de capitalização. Nosso simulador considera impostos e inflação para projeções mais precisas.',
    category: 'Renda Fixa',
    tags: ['cálculo', 'rendimento', 'cdi', 'ipca']
  },
  {
    id: '2',
    question: 'Qual a diferença entre CDI e IPCA+?',
    answer: 'CDI é uma taxa que acompanha a Selic, ideal para proteção em cenários de alta de juros. IPCA+ oferece proteção contra inflação mais um prêmio, sendo melhor para prazos longos em cenários de juros estáveis.',
    category: 'Renda Fixa',
    tags: ['cdi', 'ipca', 'diferença', 'taxas']
  },
  {
    id: '3',
    question: 'Como funcionam os fundos imobiliários?',
    answer: 'FIIs são fundos que investem em imóveis ou títulos do setor imobiliário. Oferecem dividendos mensais (dividend yield) e potencial de valorização das cotas. São isentos de IR para pessoas físicas nos dividendos.',
    category: 'Imobiliário',
    tags: ['fii', 'dividendos', 'yield', 'imóveis']
  },
  {
    id: '4',
    question: 'O que é otimização de portfolio?',
    answer: 'É a estratégia de combinar diferentes tipos de investimentos para maximizar retornos e minimizar riscos, baseada na teoria moderna de portfolios e no perfil do investidor.',
    category: 'Otimização',
    tags: ['portfolio', 'diversificação', 'risco', 'retorno']
  },
  {
    id: '5',
    question: 'Como interpretar os gráficos de resultados?',
    answer: 'Os gráficos mostram a evolução do patrimônio ao longo do tempo. Linhas mais altas indicam maior rentabilidade, enquanto a inclinação mostra a velocidade de crescimento. Compare múltiplas estratégias para ver qual se adequa melhor.',
    category: 'Análise',
    tags: ['gráficos', 'resultados', 'análise', 'interpretação']
  }
];

const tutorials: Tutorial[] = [
  {
    id: '1',
    title: 'Primeiros Passos com Renda Fixa',
    description: 'Aprenda a configurar sua primeira simulação de investimento conservador',
    duration: '5 min',
    level: 'Iniciante',
    icon: TrendingUp,
    steps: [
      'Acesse o simulador de Renda Fixa',
      'Configure o valor inicial e aportes mensais',
      'Escolha entre CDI ou IPCA+',
      'Defina o prazo de investimento',
      'Execute a simulação e analise os resultados'
    ]
  },
  {
    id: '2',
    title: 'Análise de Fundos Imobiliários',
    description: 'Como simular investimentos em FIIs e calcular dividend yield',
    duration: '8 min',
    level: 'Intermediário',
    icon: Building,
    steps: [
      'Entre no simulador Imobiliário',
      'Configure o valor do investimento',
      'Defina a taxa de dividend yield esperada',
      'Configure a valorização das cotas',
      'Analise os resultados de renda e valorização'
    ]
  },
  {
    id: '3',
    title: 'Otimização Avançada de Portfolio',
    description: 'Combine múltiplas estratégias para maximizar seus retornos',
    duration: '12 min',
    level: 'Avançado',
    icon: Target,
    steps: [
      'Execute simulações em diferentes categorias',
      'Acesse o otimizador de portfolio',
      'Configure os pesos de cada estratégia',
      'Ajuste o perfil de risco desejado',
      'Compare os resultados otimizados'
    ]
  }
];

export const HelpCenter = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [openItems, setOpenItems] = useState<string[]>([]);

  const categories = ['all', ...new Set(faqs.map(faq => faq.category))];
  
  const filteredFAQs = faqs.filter(faq => {
    const matchesSearch = faq.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         faq.answer.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         faq.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesCategory = selectedCategory === 'all' || faq.category === selectedCategory;
    
    return matchesSearch && matchesCategory;
  });

  const toggleItem = (itemId: string) => {
    setOpenItems(prev => 
      prev.includes(itemId) 
        ? prev.filter(id => id !== itemId)
        : [...prev, itemId]
    );
  };

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'Iniciante':
        return 'bg-success text-success-foreground';
      case 'Intermediário':
        return 'bg-warning text-warning-foreground';
      case 'Avançado':
        return 'bg-primary text-primary-foreground';
      default:
        return 'bg-muted text-muted-foreground';
    }
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm" className="gap-2">
          <HelpCircle className="h-4 w-4" />
          Central de Ajuda
        </Button>
      </DialogTrigger>
      
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-hidden">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <BookOpen className="h-5 w-5" />
            Central de Ajuda
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6 overflow-y-auto max-h-[calc(90vh-8rem)]">
          {/* Search */}
          <div className="space-y-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Pesquisar dúvidas ou tutoriais..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>

            {/* Category Filter */}
            <div className="flex flex-wrap gap-2">
              {categories.map(category => (
                <Button
                  key={category}
                  variant={selectedCategory === category ? "default" : "outline"}
                  size="sm"
                  onClick={() => setSelectedCategory(category)}
                >
                  {category === 'all' ? 'Todas' : category}
                </Button>
              ))}
            </div>
          </div>

          {/* Quick Start Tutorials */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <Play className="h-5 w-5" />
              Tutoriais Rápidos
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {tutorials.map(tutorial => {
                const Icon = tutorial.icon;
                return (
                  <Card key={tutorial.id} className="hover:shadow-elevated transition-shadow cursor-pointer">
                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between mb-2">
                        <div className="p-2 bg-primary/10 rounded-lg">
                          <Icon className="h-5 w-5 text-primary" />
                        </div>
                        <Badge className={getLevelColor(tutorial.level)}>
                          {tutorial.level}
                        </Badge>
                      </div>
                      
                      <CardTitle className="text-base">{tutorial.title}</CardTitle>
                      <p className="text-sm text-muted-foreground">
                        {tutorial.description}
                      </p>
                    </CardHeader>
                    
                    <CardContent className="pt-0">
                      <div className="space-y-3">
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-muted-foreground">Duração:</span>
                          <span className="font-medium">{tutorial.duration}</span>
                        </div>
                        
                        <Collapsible>
                          <CollapsibleTrigger asChild>
                            <Button variant="outline" size="sm" className="w-full justify-between">
                              Ver Passos
                              <ChevronDown className="h-4 w-4" />
                            </Button>
                          </CollapsibleTrigger>
                          <CollapsibleContent className="mt-2">
                            <ol className="space-y-1 text-sm">
                              {tutorial.steps.map((step, index) => (
                                <li key={index} className="flex items-start gap-2">
                                  <span className="w-5 h-5 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">
                                    {index + 1}
                                  </span>
                                  <span>{step}</span>
                                </li>
                              ))}
                            </ol>
                          </CollapsibleContent>
                        </Collapsible>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>

          {/* FAQ Section */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <HelpCircle className="h-5 w-5" />
              Perguntas Frequentes
            </h3>

            {filteredFAQs.length === 0 ? (
              <Card className="border-dashed">
                <CardContent className="text-center py-8">
                  <HelpCircle className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <h4 className="font-medium text-muted-foreground mb-2">
                    Nenhuma pergunta encontrada
                  </h4>
                  <p className="text-sm text-muted-foreground">
                    Tente ajustar sua pesquisa ou categoria
                  </p>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-3">
                {filteredFAQs.map(faq => (
                  <Collapsible
                    key={faq.id}
                    open={openItems.includes(faq.id)}
                    onOpenChange={() => toggleItem(faq.id)}
                  >
                    <Card>
                      <CollapsibleTrigger asChild>
                        <CardHeader className="cursor-pointer hover:bg-muted/50 transition-colors">
                          <div className="flex items-center justify-between">
                            <div className="text-left space-y-2">
                              <CardTitle className="text-base font-medium">
                                {faq.question}
                              </CardTitle>
                              <div className="flex items-center gap-2">
                                <Badge variant="secondary" className="text-xs">
                                  {faq.category}
                                </Badge>
                                <div className="flex gap-1">
                                  {faq.tags.slice(0, 3).map(tag => (
                                    <span key={tag} className="text-xs text-muted-foreground">
                                      #{tag}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            </div>
                            <ChevronDown className={`h-4 w-4 transition-transform ${
                              openItems.includes(faq.id) ? 'rotate-180' : ''
                            }`} />
                          </div>
                        </CardHeader>
                      </CollapsibleTrigger>
                      
                      <CollapsibleContent>
                        <CardContent className="pt-0">
                          <p className="text-muted-foreground leading-relaxed">
                            {faq.answer}
                          </p>
                        </CardContent>
                      </CollapsibleContent>
                    </Card>
                  </Collapsible>
                ))}
              </div>
            )}
          </div>

          {/* External Resources */}
          <Card className="bg-gradient-to-r from-primary/5 to-accent/5">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ExternalLink className="h-5 w-5" />
                Recursos Adicionais
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <p className="text-muted-foreground">
                  Aprenda mais sobre investimentos com recursos externos confiáveis:
                </p>
                
                <div className="space-y-2">
                  <Button variant="outline" size="sm" className="justify-start" asChild>
                    <a href="https://www.investidor.gov.br" target="_blank" rel="noopener noreferrer">
                      <ExternalLink className="h-4 w-4 mr-2" />
                      Portal do Investidor - CVM
                    </a>
                  </Button>
                  
                  <Button variant="outline" size="sm" className="justify-start" asChild>
                    <a href="https://www.tesourodireto.com.br" target="_blank" rel="noopener noreferrer">
                      <ExternalLink className="h-4 w-4 mr-2" />
                      Tesouro Direto
                    </a>
                  </Button>
                  
                  <Button variant="outline" size="sm" className="justify-start" asChild>
                    <a href="https://fiis.com.br" target="_blank" rel="noopener noreferrer">
                      <ExternalLink className="h-4 w-4 mr-2" />
                      Portal de FIIs
                    </a>
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </DialogContent>
    </Dialog>
  );
};