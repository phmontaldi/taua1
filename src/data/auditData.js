export const AUDIT = [
  {
    id: "A", title: "A · Organização e Preparo", max: 60,
    items: [
      { id: "A1", label: "A1. Qualidade e Consistência do Pré-Batch", max: 25,
        desc: "Sabor fiel à receita, validade, armazenamento correto." },
      { id: "A2", label: "A2. Mise en Place de Alto Volume", max: 20,
        desc: "Estoque robusto de frutas, guarnições e gelo para o dia." },
      { id: "A3", label: "A3. Organização da Estação para Agilidade", max: 15,
        desc: "Layout otimizado para minimizar movimentos e acelerar a entrega." },
    ]
  },
  {
    id: "B", title: "B · Produto e Qualidade", max: 50,
    items: [
      { id: "B1", label: "B1. Padrão de Montagem e Dosagem", max: 20,
        desc: "Uso correto do pré-batch, finalização com mixers, gelo." },
      { id: "B2", label: "B2. Apresentação Final da Bebida", max: 15,
        desc: "Copo correto, guarnição fresca, apelo visual rápido." },
      { id: "B3", label: "B3. Qualidade do Gelo e Insumos Frescos", max: 15,
        desc: "Gelo sem sabor/cheiro, frutas e sucos com aparência fresca." },
    ]
  },
  {
    id: "C", title: "C · Serviço e Ambiente", max: 60,
    items: [
      { id: "C1", label: "C1. Agilidade e Velocidade no Atendimento", max: 25,
        desc: "Tempo mínimo entre pedido e entrega." },
      { id: "C2", label: "C2. Limpeza Constante da Área de Bar", max: 20,
        desc: "Manter balcões secos, recolher copos, organização visual." },
      { id: "C3", label: "C3. Cordialidade e Energia da Equipe", max: 15,
        desc: "Atendimento positivo e proativo, mesmo sob pressão." },
    ]
  },
  {
    id: "D", title: "D · Segurança e Boas Práticas", max: 30,
    items: [
      { id: "D1", label: "D1. Boas Práticas de Higiene e Manipulação", max: 15,
        desc: "Uso de pinças/pegadores, limpeza de utensílios." },
      { id: "D2", label: "D2. Armazenamento e Validade de Produtos", max: 15,
        desc: "Principalmente dos pré-batches e sucos." },
    ]
  },
];

export const SCALE = [
  { label: "Louvor",       range: "190–200", min: 190, color: "#003D32", bg: "#d4f0e8" },
  { label: "Muito Bom",    range: "170–189", min: 170, color: "#1a6b4a", bg: "#ddf0e5" },
  { label: "Bom",          range: "150–169", min: 150, color: "#2d7a5f", bg: "#e8f5ef" },
  { label: "Regular",      range: "120–149", min: 120, color: "#b8860b", bg: "#fef3cc" },
  { label: "Insuficiente", range: "80–119",  min: 80,  color: "#cc6600", bg: "#fde8cc" },
  { label: "Deficiente",   range: "0–79",    min: 0,   color: "#b22222", bg: "#fde0e0" },
];
