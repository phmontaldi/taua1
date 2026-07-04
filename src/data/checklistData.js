export const SECTIONS = [
  {
    id: "eq", icon: "⚙️", title: "1 · Equipamentos",
    items: [
      { id: "eq1", label: "Máquina de gelo — temperatura verificada", critical: true },
      { id: "eq2", label: "Geladeira 1 — temperatura verificada", critical: true },
      { id: "eq3", label: "Geladeira 2 — temperatura verificada", critical: true },
      { id: "eq4", label: "Liquidificador funcionando", critical: true },
    ]
  },
  {
    id: "da", icon: "🥃", title: "2A · Destilados e Licores",
    items: [
      { id: "da1", label: "Vodka Skyy (padrão)", critical: true },
      { id: "da2", label: "Vodka Absolut" },
      { id: "da3", label: "Vodka Ciroc" },
      { id: "da4", label: "Gin Beefeater (padrão)", critical: true },
      { id: "da5", label: "Gin Tanqueray" },
      { id: "da6", label: "Rum Bacardi Carta Blanca" },
      { id: "da7", label: "Cachaça Sagatiba (padrão)", critical: true },
      { id: "da8", label: "Cachaça Matuta" },
      { id: "da9", label: "Cachaça Matuta Amburana" },
      { id: "da10", label: "Cachaça Matuta Mel e Limão" },
      { id: "da11", label: "Cachaça Matuta Canela" },
      { id: "da12", label: "Tequila El Jimador Blanco" },
      { id: "da13", label: "Tequila El Jimador Reposado" },
      { id: "da14", label: "Campari", critical: true },
      { id: "da15", label: "Aperol", critical: true },
      { id: "da16", label: "Licor 43" },
      { id: "da17", label: "Licor Amarula" },
      { id: "da18", label: "Vermouth 1757 (Negroni)", critical: true },
      { id: "da19", label: "Vermouth Cinzano (Negroni)", critical: true },
      { id: "da20", label: "Espumante / Prosecco (Aperol Spritz)", critical: true },
      { id: "da21", label: "Triple Sec / Cointreau (Margarita)" },
      { id: "da22", label: "JW Red Label" },
      { id: "da23", label: "JW Black Label" },
      { id: "da24", label: "JW Green Label" },
      { id: "da25", label: "JW Gold Label" },
      { id: "da26", label: "JW Blue Label" },
      { id: "da27", label: "Chivas 12 anos" },
      { id: "da28", label: "Chivas 18 anos" },
      { id: "da29", label: "Macallan 12 Sherry Oak" },
      { id: "da30", label: "Jack Daniel's" },
      { id: "da31", label: "Wild Turkey 101" },
    ]
  },
  {
    id: "sb", icon: "🍺", title: "2B · Softs e Cervejas",
    items: [
      { id: "sb1", label: "Água mineral", critical: true },
      { id: "sb2", label: "Água com gás" },
      { id: "sb3", label: "Água tônica", critical: true },
      { id: "sb4", label: "Red Bull", critical: true },
      { id: "sb5", label: "Red Bull Zero" },
      { id: "sb6", label: "Gatorade" },
      { id: "sb7", label: "Sucos lata" },
      { id: "sb8", label: "Refrigerantes", critical: true },
      { id: "sb9", label: "Heineken Lata", critical: true },
      { id: "sb10", label: "Heineken Zero" },
      { id: "sb11", label: "Amstel Lata", critical: true },
      { id: "sb12", label: "Einsebanh Lata" },
      { id: "sb13", label: "Cerveja sem Glúten" },
      { id: "sb14", label: "Chopp — barril verificado", critical: true },
    ]
  },
  {
    id: "fr", icon: "🍋", title: "2C · Frutas e Perecíveis",
    items: [
      { id: "fr1", label: "Limão Tahiti", critical: true },
      { id: "fr2", label: "Limão Siciliano", critical: true },
      { id: "fr3", label: "Laranja" },
      { id: "fr4", label: "Abacaxi", critical: true },
      { id: "fr5", label: "Caju" },
      { id: "fr6", label: "Morango (fresco)" },
      { id: "fr7", label: "Cajá (fresco)" },
      { id: "fr8", label: "Coco — água e carne (Nevada)" },
      { id: "fr9", label: "Maracujá — polpa", critical: true },
      { id: "fr10", label: "Hortelã fresca (Mojito)" },
      { id: "fr11", label: "Suco de abacaxi (Pina Colada)" },
      { id: "fr12", label: "Creme de coco (Pina Colada)" },
      { id: "fr13", label: "Leite condensado (Nevada)" },
    ]
  },
  {
    id: "pr", icon: "🧪", title: "2D · Preparados e Secos",
    items: [
      { id: "pr1", label: "Espuma de gengibre (Moscow Mule)", critical: true },
      { id: "pr2", label: "Xarope simples", critical: true },
      { id: "pr3", label: "Açúcar cristal" },
      { id: "pr4", label: "Açúcar demerara" },
      { id: "pr5", label: "Rapadura (Caipirinha Especial)" },
      { id: "pr6", label: "Sal grosso (borda Margarita)" },
    ]
  },
  {
    id: "dc", icon: "🥄", title: "2E · Descartáveis e Serviço",
    items: [
      { id: "dc1", label: "Canudos", critical: true },
      { id: "dc2", label: "Ramekin — Ketchup" },
      { id: "dc3", label: "Ramekin — Mostarda" },
      { id: "dc4", label: "Ramekin — Maionese" },
      { id: "dc5", label: "Guardanapos", critical: true },
      { id: "dc6", label: "Palitos de dente" },
      { id: "dc7", label: "Garfos descartáveis" },
      { id: "dc8", label: "Facas descartáveis" },
      { id: "dc9", label: "Colheres" },
    ]
  },
  {
    id: "cp", icon: "🥂", title: "2F · Par Estoque de Copos",
    items: [
      { id: "cp1", label: "Par estoque de copos verificado", critical: true },
    ]
  },
  {
    id: "lp", icon: "🧹", title: "3 · Limpeza e Higienização",
    items: [
      { id: "lp1", label: "Bancada higienizada", critical: true },
      { id: "lp2", label: "Coqueteleiras e utensílios limpos", critical: true },
      { id: "lp3", label: "Piso e entorno do bar", critical: true },
    ]
  },
  {
    id: "gl", icon: "🧊", title: "4 · Gelo",
    items: [
      { id: "gl1", label: "Quantidade de gelo suficiente verificada", critical: true },
      { id: "gl2", label: "Gelo reposto (se necessário)" },
      { id: "gl3", label: "Gelo nas cubas/baldes da estação", critical: true },
    ]
  },
  {
    id: "ct", icon: "🔪", title: "5 · Corte e Preparo de Frutas",
    items: [
      { id: "ct1", label: "Caju — cubos médios", critical: true },
      { id: "ct2", label: "Abacaxi — cubos médios", critical: true },
      { id: "ct3", label: "Laranja — meia-lua", critical: true },
      { id: "ct4", label: "Limão Siciliano — meia-lua", critical: true },
      { id: "ct5", label: "Morango — higienizado, sem corte" },
      { id: "ct6", label: "Cajá — higienizado, sem corte" },
      { id: "ct7", label: "Limão Tahiti — reservar, cortar na hora", critical: true },
      { id: "ct8", label: "Maracujá — polpa no store and pour", critical: true },
    ]
  },
  {
    id: "es", icon: "🎯", title: "6 · Montagem da Estação",
    items: [
      { id: "es1", label: "Gelo nas cubas confirmado", critical: true },
      { id: "es2", label: "Ferramentas no lugar (coqueteleira, jigger, muddler, colher, abridor)", critical: true },
      { id: "es3", label: "Frutas e preparados posicionados", critical: true },
      { id: "es4", label: "Descartáveis e condimentos no lugar", critical: true },
    ]
  },
];
