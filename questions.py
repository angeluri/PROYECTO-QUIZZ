"""
questions.py – Contenido educativo configurable.
5 cursos × 5 módulos × 10 preguntas = 250 preguntas sobre vida saludable.
Estructura: COURSES = { "Curso": { "Módulo": [lista de preguntas] } }
Cada pregunta: question, options (lista), answer (índice 0-3), explanation.
"""

COURSES = {
    "Nutrición y Alimentación Saludable": {
        "Fundamentos de Nutrición": [
            {
                "question": "¿Cuál de los siguientes es un macronutriente?",
                "options": ["Vitamina C", "Calcio", "Proteína", "Fibra"],
                "answer": 2,
                "explanation": "Las proteínas son macronutrientes junto con carbohidratos y grasas."
            },
            {
                "question": "¿Qué nutriente proporciona la mayor cantidad de energía por gramo?",
                "options": ["Carbohidratos", "Proteínas", "Grasas", "Vitaminas"],
                "answer": 2,
                "explanation": "Las grasas aportan 9 kcal/g, mientras que carbohidratos y proteínas 4 kcal/g."
            },
            {
                "question": "¿Cuál es la función principal de los carbohidratos?",
                "options": ["Construir tejidos", "Energía rápida", "Transportar vitaminas", "Regular la temperatura"],
                "answer": 1,
                "explanation": "Los carbohidratos se convierten en glucosa, fuente primaria de energía."
            },
            {
                "question": "¿Qué porcentaje de la dieta diaria deberían representar los carbohidratos según guías saludables?",
                "options": ["10-15%", "25-30%", "45-65%", "70-80%"],
                "answer": 2,
                "explanation": "Las guías recomiendan que los carbohidratos aporten entre 45-65% de las calorías totales."
            },
            {
                "question": "¿Cuál es un ejemplo de carbohidrato complejo?",
                "options": ["Azúcar blanca", "Miel", "Pan integral", "Jugo de naranja"],
                "answer": 2,
                "explanation": "El pan integral contiene almidón y fibra, liberando energía gradualmente."
            },
            {
                "question": "¿Qué tipo de grasa es líquida a temperatura ambiente?",
                "options": ["Saturada", "Trans", "Insaturada", "Hidrogenada"],
                "answer": 2,
                "explanation": "Las grasas insaturadas (aceites vegetales) son líquidas a temperatura ambiente."
            },
            {
                "question": "¿Cuál es el aminoácido esencial más común en deficiencia en dietas vegetarianas?",
                "options": ["Lisina", "Metionina", "Triptófano", "Leucina"],
                "answer": 0,
                "explanation": "La lisina es limitada en cereales, pero abundante en legumbres."
            },
            {
                "question": "¿Cuántos aminoácidos esenciales necesita el ser humano?",
                "options": ["5", "8", "9", "12"],
                "answer": 2,
                "explanation": "Existen 9 aminoácidos esenciales que el cuerpo no puede sintetizar."
            },
            {
                "question": "¿Qué sucede con el exceso de proteína consumida?",
                "options": ["Se almacena como músculo", "Se convierte en grasa o se excreta", "Se elimina sin cambios", "Se convierte en vitaminas"],
                "answer": 1,
                "explanation": "El exceso de proteína se desamina y el nitrógeno se excreta; el resto puede convertirse en grasa."
            },
            {
                "question": "¿Qué dieta se asocia con menor riesgo de enfermedades cardiovasculares?",
                "options": ["Alta en carnes rojas", "Alta en azúcares refinados", "Mediterránea", "Alta en grasas trans"],
                "answer": 2,
                "explanation": "La dieta mediterránea es rica en frutas, verduras, aceite de oliva y pescado."
            }
        ],
        "Macronutrientes y Micronutrientes": [
            {
                "question": "¿Qué vitamina es liposoluble?",
                "options": ["Vitamina C", "Vitamina B12", "Vitamina D", "Vitamina B6"],
                "answer": 2,
                "explanation": "Las vitaminas A, D, E y K son liposolubles y se almacenan en tejido graso."
            },
            {
                "question": "¿Cuál es la principal fuente dietética de vitamina B12?",
                "options": ["Frutas", "Verduras de hoja", "Carnes y lácteos", "Cereales integrales"],
                "answer": 2,
                "explanation": "La vitamina B12 se encuentra en alimentos de origen animal; los vegetarianos estrictos necesitan suplementos."
            },
            {
                "question": "¿Qué mineral es crucial para la función tiroidea?",
                "options": ["Hierro", "Yodo", "Zinc", "Selenio"],
                "answer": 1,
                "explanation": "El yodo es componente de las hormonas tiroideas T3 y T4."
            },
            {
                "question": "¿Cuál es una consecuencia de la deficiencia de vitamina A?",
                "options": ["Raquitismo", "Anemia perniciosa", "Ceguera nocturna", "Escorbuto"],
                "answer": 2,
                "explanation": "La vitamina A es esencial para los fotorreceptores de la retina."
            },
            {
                "question": "¿Qué alimento es rico en zinc?",
                "options": ["Manzana", "Lechuga", "Ostras", "Pan blanco"],
                "answer": 2,
                "explanation": "Las ostras y otros mariscos tienen alta concentración de zinc."
            },
            {
                "question": "¿Cuál es la función del magnesio en el cuerpo?",
                "options": ["Coagulación sanguínea", "Contracción muscular y función nerviosa", "Transporte de oxígeno", "Síntesis de colágeno"],
                "answer": 1,
                "explanation": "El magnesio participa en más de 300 reacciones enzimáticas, incluyendo contracción muscular."
            },
            {
                "question": "¿Qué vitamina actúa como antioxidante protegiendo membranas celulares?",
                "options": ["Vitamina B1", "Vitamina E", "Vitamina K", "Vitamina B3"],
                "answer": 1,
                "explanation": "La vitamina E (tocoferol) protege los ácidos grasos poliinsaturados de la oxidación."
            },
            {
                "question": "¿Qué mineral ayuda a regular la presión arterial?",
                "options": ["Sodio (en exceso)", "Potasio", "Cloro", "Fósforo"],
                "answer": 1,
                "explanation": "El potasio contrarresta los efectos del sodio y ayuda a bajar la presión arterial."
            },
            {
                "question": "¿Qué deficiencia de vitamina causa el escorbuto?",
                "options": ["Vitamina A", "Vitamina C", "Vitamina D", "Vitamina B12"],
                "answer": 1,
                "explanation": "La falta de vitamina C produce escorbuto, con sangrado de encías y mala cicatrización."
            },
            {
                "question": "¿Cuál es la fuente más rica en calcio biodisponible?",
                "options": ["Espinaca", "Leche y derivados", "Almendras", "Brócoli"],
                "answer": 1,
                "explanation": "Los lácteos tienen alta biodisponibilidad de calcio comparado con vegetales."
            }
        ],
        "Alimentos Funcionales y Fibra": [
            {
                "question": "¿Qué tipo de fibra ayuda a reducir el colesterol?",
                "options": ["Fibra insoluble", "Fibra soluble", "Celulosa", "Lignina"],
                "answer": 1,
                "explanation": "La fibra soluble forma un gel que atrapa ácidos biliares y colesterol."
            },
            {
                "question": "¿Cuál de estos alimentos es un prebiótico natural?",
                "options": ["Yogur", "Ajo", "Queso", "Carne de res"],
                "answer": 1,
                "explanation": "El ajo contiene inulina, un prebiótico que alimenta bacterias beneficiosas."
            },
            {
                "question": "¿Qué es un probiótico?",
                "options": ["Fibra no digerible", "Microorganismo vivo beneficioso", "Enzima digestiva", "Antibiótico natural"],
                "answer": 1,
                "explanation": "Los probióticos son bacterias vivas que mejoran la microbiota intestinal."
            },
            {
                "question": "¿Cuál es un beneficio de la fibra insoluble?",
                "options": ["Reduce el estreñimiento", "Baja el colesterol", "Aporta calorías", "Aumenta el azúcar"],
                "answer": 0,
                "explanation": "La fibra insoluble (salvado de trigo) acelera el tránsito intestinal."
            },
            {
                "question": "¿Qué alimentos son ricos en antioxidantes?",
                "options": ["Papas fritas", "Bayas y frutos rojos", "Pan blanco", "Carne procesada"],
                "answer": 1,
                "explanation": "Las bayas contienen antocianinas y otros polifenoles antioxidantes."
            },
            {
                "question": "¿Cuál es el principal efecto de los fitoesteroles?",
                "options": ["Aumentar el colesterol", "Reducir la absorción de colesterol", "Mejorar la digestión de proteínas", "Aumentar la masa muscular"],
                "answer": 1,
                "explanation": "Los fitoesteroles compiten con el colesterol en la absorción intestinal."
            },
            {
                "question": "¿Qué compuesto del té verde se asocia con beneficios metabólicos?",
                "options": ["Teobromina", "Cafeína", "EGCG (galato de epigalocatequina)", "L-teanina"],
                "answer": 2,
                "explanation": "El EGCG es un catequina con propiedades antioxidantes y termogénicas."
            },
            {
                "question": "¿Cuál es un alimento fermentado beneficioso para la salud intestinal?",
                "options": ["Pepinillos en vinagre", "Kéfir", "Jamón serrano", "Pan de molde"],
                "answer": 1,
                "explanation": "El kéfir contiene múltiples cepas de bacterias y levaduras probióticas."
            },
            {
                "question": "¿Qué cantidad de fibra diaria se recomienda para adultos?",
                "options": ["5-10 g", "15-20 g", "25-35 g", "45-50 g"],
                "answer": 2,
                "explanation": "La mayoría de guías recomiendan 25-35 gramos de fibra al día."
            },
            {
                "question": "¿Qué tipo de chocolate tiene mayor contenido de flavonoides?",
                "options": ["Chocolate blanco", "Chocolate con leche", "Chocolate oscuro (>70% cacao)", "Chocolate de repostería"],
                "answer": 2,
                "explanation": "El chocolate oscuro conserva más flavonoides del cacao."
            }
        ],
        "Hidratación y Bebidas": [
            {
                "question": "¿Qué porcentaje del cuerpo humano adulto es agua aproximadamente?",
                "options": ["40%", "50%", "60%", "75%"],
                "answer": 2,
                "explanation": "El agua representa alrededor del 60% del peso corporal en adultos."
            },
            {
                "question": "¿Cuál es la recomendación diaria de agua para un adulto en clima templado?",
                "options": ["1-2 litros", "2-3 litros", "4-5 litros", "Más de 6 litros"],
                "answer": 1,
                "explanation": "Se recomiendan aproximadamente 2-3 litros totales de agua (incluyendo alimentos)."
            },
            {
                "question": "¿Qué signo indica deshidratación leve?",
                "options": ["Orina clara", "Sed y orina oscura", "Hinchazón", "Fiebre alta"],
                "answer": 1,
                "explanation": "La orina oscura y la sed son signos tempranos de deshidratación."
            },
            {
                "question": "¿Qué bebida hidrata más eficazmente después del ejercicio intenso?",
                "options": ["Agua sola", "Bebida deportiva con electrolitos", "Café", "Cerveza"],
                "answer": 1,
                "explanation": "Las bebidas con electrolitos reponen sodio y potasio perdidos en el sudor."
            },
            {
                "question": "¿Qué efecto tiene el alcohol en la hidratación?",
                "options": ["Aumenta la retención de agua", "Es diurético y deshidrata", "No afecta", "Mejora la absorción"],
                "answer": 1,
                "explanation": "El alcohol inhibe la hormona antidiurética, aumentando la pérdida de agua."
            },
            {
                "question": "¿Cuál es la mejor manera de saber si estás bien hidratado?",
                "options": ["Peso corporal", "Color de la orina", "Temperatura de la piel", "Frecuencia cardíaca"],
                "answer": 1,
                "explanation": "El color amarillo claro de la orina indica buena hidratación."
            },
            {
                "question": "¿Qué bebida tiene un efecto diurético suave pero también aporta antioxidantes?",
                "options": ["Café", "Té verde", "Leche", "Refresco cola"],
                "answer": 1,
                "explanation": "El té verde contiene cafeína (diurética) y catequinas antioxidantes."
            },
            {
                "question": "¿Cuánta agua se pierde diariamente por respiración y sudor insensible?",
                "options": ["200-300 ml", "500-800 ml", "1-1.5 litros", "2 litros"],
                "answer": 1,
                "explanation": "La pérdida insensible (sin contar sudor visible) es de 500-800 ml/día."
            },
            {
                "question": "¿Qué población tiene mayor riesgo de deshidratación?",
                "options": ["Adultos jóvenes", "Deportistas bien entrenados", "Adultos mayores", "Adolescentes"],
                "answer": 2,
                "explanation": "Los adultos mayores tienen menor sensación de sed y función renal disminuida."
            },
            {
                "question": "¿Qué bebida se debe evitar en climas calurosos por su efecto deshidratante?",
                "options": ["Agua de coco", "Agua simple", "Bebidas alcohólicas", "Jugo natural"],
                "answer": 2,
                "explanation": "El alcohol aumenta la diuresis y puede acelerar la deshidratación."
            }
        ],
        "Planificación de Comidas y Dietas Especiales": [
            {
                "question": "¿Qué es el índice glucémico?",
                "options": ["Cantidad de azúcar en un alimento", "Velocidad de elevación del azúcar en sangre", "Contenido de fibra", "Densidad calórica"],
                "answer": 1,
                "explanation": "Mide qué tan rápido eleva la glucosa en sangre un alimento."
            },
            {
                "question": "¿Cuál de estas dietas ha demostrado eficacia para controlar la diabetes tipo 2?",
                "options": ["Alta en azúcares", "Baja en carbohidratos (moderada)", "Alta en grasas saturadas", "Jugoterapia exclusiva"],
                "answer": 1,
                "explanation": "Una dieta baja en carbohidratos mejora el control glucémico."
            },
            {
                "question": "¿Qué patrón de alimentación recomienda la dieta DASH?",
                "options": ["Alta en sodio", "Rica en frutas, verduras y baja en grasas saturadas", "Alta en carnes rojas", "Ayuno intermitente estricto"],
                "answer": 1,
                "explanation": "DASH es efectiva para la hipertensión, con énfasis en potasio y bajo sodio."
            },
            {
                "question": "¿Qué grupo de alimentos debe limitarse en una dieta baja en FODMAP?",
                "options": ["Frutas bajas en fructosa", "Verduras crucíferas", "Arroz", "Carnes magras"],
                "answer": 1,
                "explanation": "Muchas verduras como brócoli, coliflor y cebolla son altas en FODMAP."
            },
            {
                "question": "¿Cuál es un principio de la dieta mediterránea?",
                "options": ["Alto consumo de grasas saturadas", "Uso de aceite de oliva como grasa principal", "Evitar el pescado", "Alto consumo de dulces"],
                "answer": 1,
                "explanation": "El aceite de oliva virgen extra es la fuente principal de grasa."
            },
            {
                "question": "¿Qué nutriente debe controlarse más en una dieta para enfermedad renal crónica?",
                "options": ["Vitamina C", "Proteína, fósforo y potasio", "Fibra", "Carbohidratos"],
                "answer": 1,
                "explanation": "Los riñones dañados no filtran adecuadamente estos nutrientes."
            },
            {
                "question": "¿Qué estrategia ayuda a reducir el consumo calórico sin dietas extremas?",
                "options": ["Saltarse el desayuno", "Usar platos más pequeños", "Beber jugos industriales", "Comer rápido"],
                "answer": 1,
                "explanation": "Platos más pequeños reducen las porciones de forma natural."
            },
            {
                "question": "¿Qué es la alimentación intuitiva?",
                "options": ["Comer solo cuando la balanza lo indica", "Escuchar señales de hambre y saciedad", "Seguir un plan rígido", "Ayunar 20 horas"],
                "answer": 1,
                "explanation": "Se basa en respetar las necesidades internas sin culpa."
            },
            {
                "question": "¿Cuál es una recomendación para el desayuno saludable?",
                "options": ["Alto en azúcares añadidos", "Incluir proteína y fibra", "Solo café", "Evitar frutas"],
                "answer": 1,
                "explanation": "Proteína y fibra proporcionan saciedad y energía sostenida."
            },
            {
                "question": "¿Qué método de cocción añade menos calorías extras?",
                "options": ["Freír", "Hervir o cocer al vapor", "Estofado con mucho aceite", "Rehogar con mantequilla"],
                "answer": 1,
                "explanation": "La cocción al vapor no requiere grasas añadidas."
            }
        ]
    },
    "Ejercicio y Actividad Física": {
        "Tipos de Ejercicio": [
            {
                "question": "¿Qué tipo de ejercicio mejora principalmente la resistencia cardiovascular?",
                "options": ["Entrenamiento de fuerza", "Ejercicio aeróbico", "Estiramientos", "Pliometría"],
                "answer": 1,
                "explanation": "El ejercicio aeróbico (correr, nadar, ciclismo) fortalece el corazón y pulmones."
            },
            {
                "question": "¿Cuál es un ejemplo de ejercicio anaeróbico?",
                "options": ["Caminata de 30 minutos", "Levantamiento de pesas a máxima intensidad", "Yoga suave", "Trote ligero"],
                "answer": 1,
                "explanation": "El ejercicio anaeróbico es de alta intensidad y corta duración, sin uso de oxígeno como fuente principal."
            },
            {
                "question": "¿Qué beneficio tiene el entrenamiento de fuerza en adultos mayores?",
                "options": ["Aumenta la fragilidad", "Previene la sarcopenia y caídas", "Disminuye la densidad ósea", "Reduce la movilidad"],
                "answer": 1,
                "explanation": "El entrenamiento de fuerza mantiene masa muscular y mejora el equilibrio."
            },
            {
                "question": "¿Qué tipo de ejercicio es mejor para la flexibilidad?",
                "options": ["Sentadillas", "Estiramientos estáticos y dinámicos", "Carrera de velocidad", "Natación"],
                "answer": 1,
                "explanation": "Los estiramientos regulares aumentan el rango de movimiento articular."
            },
            {
                "question": "¿Qué es el entrenamiento funcional?",
                "options": ["Ejercicios de máquinas aisladas", "Movimientos que imitan actividades diarias", "Solo cardio", "Levantamiento olímpico"],
                "answer": 1,
                "explanation": "Mejora la capacidad para realizar tareas cotidianas (subir escaleras, cargar compras)."
            },
            {
                "question": "¿Cuál es un deporte de bajo impacto recomendado para personas con artritis?",
                "options": ["Saltar la cuerda", "Natación", "Correr en asfalto", "Crossfit"],
                "answer": 1,
                "explanation": "La natación no carga las articulaciones y mejora la movilidad."
            },
            {
                "question": "¿Qué es la frecuencia cardíaca máxima teórica?",
                "options": ["220 - edad", "200 - edad", "180 - edad", "240 - edad"],
                "answer": 0,
                "explanation": "La fórmula común es 220 - edad (años), aunque varía según individuos."
            },
            {
                "question": "¿Qué intensidad se considera actividad física vigorosa?",
                "options": ["Hablar con facilidad", "No poder hablar sin pausas", "Caminar despacio", "Lavar platos"],
                "answer": 1,
                "explanation": "A intensidad vigorosa, la respiración es muy rápida y no se puede mantener una conversación."
            },
            {
                "question": "¿Qué tipo de ejercicio quema más calorías por minuto?",
                "options": ["Caminar a 5 km/h", "Correr a 10 km/h", "Yoga restaurativo", "Estiramientos"],
                "answer": 1,
                "explanation": "Correr a mayor velocidad requiere más energía por minuto."
            },
            {
                "question": "¿Qué es el EPOC (exceso de consumo de oxígeno post-ejercicio)?",
                "options": ["Fatiga muscular", "Quema de calorías después del ejercicio", "Lesión por sobreuso", "Falta de oxígeno durante el ejercicio"],
                "answer": 1,
                "explanation": "El cuerpo sigue consumiendo más oxígeno y quemando calorías tras el ejercicio intenso."
            }
        ],
        "Entrenamiento Cardiovascular": [
            {
                "question": "¿Cuál es la frecuencia cardíaca objetivo para mejorar la salud cardiovascular en adultos?",
                "options": ["50-70% de la FC máxima", "80-90%", "30-40%", "Menos del 30%"],
                "answer": 0,
                "explanation": "La zona de intensidad moderada (50-70%) es ideal para principiantes y salud general."
            },
            {
                "question": "¿Cuántos minutos semanales de cardio moderado reducen significativamente el riesgo cardiovascular?",
                "options": ["75 minutos", "150 minutos", "300 minutos", "30 minutos"],
                "answer": 1,
                "explanation": "150 minutos semanales es la recomendación mínima de la OMS."
            },
            {
                "question": "¿Qué prueba es estándar para medir la capacidad aeróbica?",
                "options": ["Test de Cooper (12 min corriendo)", "Flexiones", "Abdominales", "Salto vertical"],
                "answer": 0,
                "explanation": "El test de Cooper estima el VO2 máximo mediante la distancia recorrida en 12 minutos."
            },
            {
                "question": "¿Qué es el entrenamiento intervalado de alta intensidad (HIIT)?",
                "options": ["Ejercicio continuo al 60%", "Alternancia de esfuerzos máximos y recuperación", "Estiramientos intensos", "Ejercicio de baja intensidad largo"],
                "answer": 1,
                "explanation": "HIIT alterna periodos de esfuerzo casi máximo con descanso activo."
            },
            {
                "question": "¿Cuál es una ventaja del HIIT sobre el cardio continuo?",
                "options": ["Menor eficiencia de tiempo", "Mayor quema de grasa post-ejercicio", "Menor adaptación cardiovascular", "Mayor riesgo de aburrimiento"],
                "answer": 1,
                "explanation": "El HIIT produce un mayor EPOC y mejora la sensibilidad a la insulina."
            },
            {
                "question": "¿Qué tipo de cardio es más adecuado para principiantes con obesidad?",
                "options": ["Carrera intensa", "Caminatas progresivas", "Saltos pliométricos", "Burpees"],
                "answer": 1,
                "explanation": "Caminar es de bajo impacto y fácil de progresar."
            },
            {
                "question": "¿Qué sucede con el corazón con el entrenamiento cardiovascular regular?",
                "options": ["Aumenta la frecuencia cardíaca en reposo", "Disminuye el tamaño del corazón", "Mejora la eficiencia de bombeo", "Aumenta la rigidez arterial"],
                "answer": 2,
                "explanation": "El corazón se vuelve más eficiente, bombeando más sangre por latido."
            },
            {
                "question": "¿Cuál es un signo de ejercicio cardiovascular excesivo?",
                "options": ["Mejor sueño", "Fatiga persistente y caída del rendimiento", "Aumento de la frecuencia cardíaca en reposo", "Ambas B y C son correctas"],
                "answer": 3,
                "explanation": "El sobreentrenamiento cardio puede causar fatiga crónica y aumento de la FC reposo."
            },
            {
                "question": "¿Qué máquina de gimnasio proporciona un entrenamiento cardiovascular de bajo impacto?",
                "options": ["Cinta de correr", "Escaladora", "Bicicleta elíptica", "Remo"],
                "answer": 2,
                "explanation": "La elíptica minimiza el impacto en rodillas y caderas."
            },
            {
                "question": "¿Qué es la 'zona de quema de grasa'?",
                "options": ["Alta intensidad (85-95% FC máx)", "Intensidad baja-moderada (50-65% FC máx)", "Reposo absoluto", "Sprint máximo"],
                "answer": 1,
                "explanation": "A baja intensidad, el porcentaje de energía proveniente de grasa es mayor, aunque el gasto total calórico es menor."
            }
        ],
        "Fuerza y Resistencia Muscular": [
            {
                "question": "¿Cuántas veces por semana se recomienda entrenar fuerza para principiantes?",
                "options": ["1 vez", "2-3 veces", "5-6 veces", "Todos los días"],
                "answer": 1,
                "explanation": "2-3 sesiones semanales permiten recuperación adecuada."
            },
            {
                "question": "¿Qué rango de repeticiones es óptimo para la hipertrofia muscular?",
                "options": ["1-5 repeticiones", "6-12 repeticiones", "15-20 repeticiones", "Más de 30 repeticiones"],
                "answer": 1,
                "explanation": "Entre 6-12 repeticiones con carga moderada-alta estimula el crecimiento muscular."
            },
            {
                "question": "¿Qué es la sobrecarga progresiva?",
                "options": ["Hacer siempre el mismo peso", "Aumentar gradualmente la exigencia", "Reducir el volumen", "Cambiar de ejercicio cada día"],
                "answer": 1,
                "explanation": "Aumentar peso, repeticiones o series de forma gradual para seguir ganando fuerza."
            },
            {
                "question": "¿Cuánto tiempo de descanso entre series para fuerza máxima?",
                "options": ["30 segundos", "1-2 minutos", "3-5 minutos", "10 minutos"],
                "answer": 2,
                "explanation": "Descansos largos (3-5 min) permiten recuperar el sistema fosfágeno para levantar pesado."
            },
            {
                "question": "¿Qué es la repetición hasta el fallo muscular?",
                "options": ["Parar cuando duele", "Llegar al punto de no poder hacer otra repetición con buena técnica", "Hacer repeticiones rápidas", "Usar impulso"],
                "answer": 1,
                "explanation": "El fallo concéntrico es cuando no se puede completar el movimiento."
            },
            {
                "question": "¿Qué beneficios aporta el entrenamiento de fuerza en la salud ósea?",
                "options": ["Disminuye la densidad mineral ósea", "Aumenta la densidad ósea previniendo osteoporosis", "No afecta los huesos", "Debilita los ligamentos"],
                "answer": 1,
                "explanation": "La carga mecánica estimula los osteoblastos, aumentando la densidad ósea."
            },
            {
                "question": "¿Qué músculo es el principal responsable de la extensión de la pierna?",
                "options": ["Isquiotibiales", "Cuádriceps", "Glúteo mayor", "Gastrocnemio"],
                "answer": 1,
                "explanation": "El cuádriceps extiende la rodilla."
            },
            {
                "question": "¿Cuál es un buen ejercicio para los músculos de la espalda (dorsales)?",
                "options": ["Press de banca", "Dominadas o jalón al pecho", "Curl de bíceps", "Elevaciones laterales"],
                "answer": 1,
                "explanation": "Las dominadas trabajan principalmente los dorsales y bíceps."
            },
            {
                "question": "¿Qué es la periodización del entrenamiento?",
                "options": ["Variación sistemática del volumen e intensidad", "Hacer siempre la misma rutina", "Entrenar hasta lesionarse", "Solo cardio"],
                "answer": 0,
                "explanation": "La periodización evita estancamientos y reduce el riesgo de sobreentrenamiento."
            },
            {
                "question": "¿Cuánto tiempo de descanso entre sesiones del mismo grupo muscular?",
                "options": ["12 horas", "24-48 horas", "5 días", "1 semana"],
                "answer": 1,
                "explanation": "Se recomienda 48 horas para recuperar completamente las fibras musculares."
            }
        ],
        "Flexibilidad y Movilidad": [
            {
                "question": "¿Cuál es la diferencia entre flexibilidad y movilidad?",
                "options": ["Son sinónimos", "Flexibilidad es pasiva, movilidad es activa con control", "Movilidad es solo articular", "Flexibilidad es fuerza"],
                "answer": 1,
                "explanation": "La movilidad implica el rango de movimiento activo y control neuromuscular."
            },
            {
                "question": "¿Qué tipo de estiramiento se recomienda antes del ejercicio?",
                "options": ["Estático mantenido", "Balístico", "Dinámico", "Pasivo con ayuda"],
                "answer": 2,
                "explanation": "Los estiramientos dinámicos aumentan la temperatura muscular y la activación."
            },
            {
                "question": "¿Cuánto tiempo debe mantenerse un estiramiento estático para mejorar la flexibilidad?",
                "options": ["5-10 segundos", "15-30 segundos", "1-2 minutos", "Más de 5 minutos"],
                "answer": 1,
                "explanation": "Mantener 15-30 segundos produce adaptaciones en la longitud muscular."
            },
            {
                "question": "¿Qué es la propiocepción?",
                "options": ["Dolor muscular", "Capacidad de sentir la posición del cuerpo", "Equilibrio visual", "Fuerza explosiva"],
                "answer": 1,
                "explanation": "Es el sentido que informa al cerebro sobre la posición de las articulaciones."
            },
            {
                "question": "¿Qué disciplina combina respiración, posturas y meditación para mejorar flexibilidad?",
                "options": ["Pilates", "Yoga", "Taichí", "Crossfit"],
                "answer": 1,
                "explanation": "El yoga incluye asanas (posturas) que mejoran flexibilidad, fuerza y equilibrio."
            },
            {
                "question": "¿Cuál es un beneficio de mejorar la movilidad de cadera?",
                "options": ["Mayor riesgo de lesión de espalda", "Mejorar la sentadilla y prevenir dolor lumbar", "Aumentar la rigidez", "Empeorar la postura"],
                "answer": 1,
                "explanation": "La movilidad de cadera evita compensaciones lumbares en movimientos como agacharse."
            },
            {
                "question": "¿Qué es el estiramiento facilitador neuromuscular propioceptivo (FNP)?",
                "options": ["Estiramiento rápido", "Técnica que combina contracción y relajación", "Masaje profundo", "Uso de vibraciones"],
                "answer": 1,
                "explanation": "FNP usa la inhibición autógena o recíproca para lograr mayor rango de movimiento."
            },
            {
                "question": "¿Con qué frecuencia se debería trabajar la flexibilidad para mejoras notables?",
                "options": ["Una vez al mes", "2-3 veces por semana", "Solo después de entrenar fuerza", "Una vez al año"],
                "answer": 1,
                "explanation": "La constancia (mínimo 2-3 sesiones semanales) produce adaptaciones."
            },
            {
                "question": "¿Qué músculo suele estar acortado en personas con mala postura de oficina?",
                "options": ["Isquiotibiales", "Psoas iliaco (flexores de cadera)", "Glúteos", "Paraespinales lumbares"],
                "answer": 1,
                "explanation": "Estar sentado acorta los flexores de cadera, contribuyendo al dolor lumbar."
            },
            {
                "question": "¿Qué herramienta se usa para el automasaje y liberación miofascial?",
                "options": ["Barra", "Rodillo de espuma (foam roller)", "Pesas rusas", "Cuerda para saltar"],
                "answer": 1,
                "explanation": "El foam roller ayuda a reducir puntos gatillo y mejorar la calidad del tejido."
            }
        ],
        "Prevención de Lesiones y Recuperación": [
            {
                "question": "¿Cuál es la causa más común de lesiones en principiantes?",
                "options": ["Mala técnica y progresión muy rápida", "Uso de pesas muy ligeras", "Estiramientos excesivos", "Entrenar solo una vez por semana"],
                "answer": 0,
                "explanation": "Aumentar carga o volumen demasiado rápido supera la capacidad de adaptación."
            },
            {
                "question": "¿Qué es el reposo activo?",
                "options": ["No hacer nada", "Actividad de baja intensidad como caminar o estiramientos", "Dormir 12 horas", "Deporte competitivo"],
                "answer": 1,
                "explanation": "El reposo activo mejora la circulación y elimina metabolitos sin estrés adicional."
            },
            {
                "question": "¿Qué hacer inmediatamente después de una torcedura de tobillo?",
                "options": ["Aplicar calor", "Movilizar forzadamente", "Aplicar hielo, compresión y elevación (RICE)", "Seguir entrenando"],
                "answer": 2,
                "explanation": "El protocolo RICE (reposo, hielo, compresión, elevación) reduce inflamación aguda."
            },
            {
                "question": "¿Qué es la tendinopatía?",
                "options": ["Inflamación del músculo", "Lesión degenerativa del tendón", "Fractura ósea", "Desgarro ligamentario"],
                "answer": 1,
                "explanation": "Las tendinopatías suelen ser por sobreuso y falta de recuperación."
            },
            {
                "question": "¿Cuál es la mejor manera de prevenir lesiones por sobreuso?",
                "options": ["Entrenar el mismo músculo todos los días", "Variar los estímulos y respetar el descanso", "Usar cargas máximas siempre", "Saltarse el calentamiento"],
                "answer": 1,
                "explanation": "La periodización y el descanso evitan la acumulación de microtraumatismos."
            },
            {
                "question": "¿Qué papel juega el calzado en la prevención de lesiones?",
                "options": ["Ninguno", "Debe ser adecuado al deporte y tipo de pisada", "Mientras más viejo mejor", "Solo importa en correr"],
                "answer": 1,
                "explanation": "Un calzado inadecuado puede causar fascitis plantar, tendinitis o fracturas por estrés."
            },
            {
                "question": "¿Qué es el síndrome de sobreentrenamiento?",
                "options": ["Mayor rendimiento", "Fatiga crónica, irritabilidad, caída del rendimiento", "Aumento de masa muscular", "Mejor sueño"],
                "answer": 1,
                "explanation": "Se produce por desbalance entre carga y recuperación, con consecuencias sistémicas."
            },
            {
                "question": "¿Cuánto tiempo de sueño se recomienda para una adecuada recuperación muscular?",
                "options": ["4-5 horas", "7-9 horas", "10-12 horas", "No influye"],
                "answer": 1,
                "explanation": "Durante el sueño profundo se libera hormona del crecimiento y se repara el tejido."
            },
            {
                "question": "¿Qué nutriente es clave para la reparación de tejidos después del ejercicio?",
                "options": ["Carbohidratos solos", "Proteínas de alta calidad", "Grasas saturadas", "Azúcares refinados"],
                "answer": 1,
                "explanation": "Las proteínas aportan aminoácidos para la síntesis de proteínas musculares."
            },
            {
                "question": "¿Qué es un desgarro muscular?",
                "options": ["Rotura de fibras musculares", "Inflamación tendinosa", "Fractura ósea", "Lesión de ligamento"],
                "answer": 0,
                "explanation": "Puede ser de grado I (leve) a III (rotura completa)."
            }
        ]
    },
    "Salud Mental y Bienestar Emocional": {
        "Manejo del Estrés": [
            {
                "question": "¿Cuál es la hormona principal liberada durante el estrés crónico?",
                "options": ["Serotonina", "Cortisol", "Dopamina", "Oxitocina"],
                "answer": 1,
                "explanation": "El cortisol elevado de forma prolongada tiene efectos negativos en el cuerpo."
            },
            {
                "question": "¿Qué técnica de respiración ayuda a reducir el estrés rápidamente?",
                "options": ["Hiperventilación", "Respiración diafragmática lenta", "Contener la respiración", "Respiración muy rápida"],
                "answer": 1,
                "explanation": "La respiración profunda activa el sistema nervioso parasimpático."
            },
            {
                "question": "¿Qué es el mindfulness?",
                "options": ["Pensar en el futuro", "Atención plena en el momento presente sin juicio", "Evitar pensamientos", "Dormir profundamente"],
                "answer": 1,
                "explanation": "Mindfulness reduce la reactividad emocional y mejora la regulación del estrés."
            },
            {
                "question": "¿Cuál es un síntoma físico del estrés agudo?",
                "options": ["Bradicardia", "Tensión muscular y aumento de frecuencia cardíaca", "Somnolencia extrema", "Hipotensión"],
                "answer": 1,
                "explanation": "La respuesta de lucha o huida activa el sistema simpático."
            },
            {
                "question": "¿Qué actividad al aire libre reduce significativamente los niveles de cortisol?",
                "options": ["Estar en ambientes naturales (baños de bosque)", "Estar en tráfico pesado", "Mirar una pantalla", "Escuchar ruido industrial"],
                "answer": 0,
                "explanation": "La exposición a la naturaleza disminuye el estrés y mejora el estado de ánimo."
            },
            {
                "question": "¿Cuántas horas de sueño se recomiendan para una buena regulación del estrés?",
                "options": ["Menos de 5", "Entre 7 y 9", "Más de 12", "No importa"],
                "answer": 1,
                "explanation": "El sueño insuficiente aumenta la reactividad al estrés y los niveles de cortisol."
            },
            {
                "question": "¿Qué es la rumiación mental?",
                "options": ["Pensar en soluciones", "Dar vueltas repetitivas a pensamientos negativos", "Meditar activamente", "Planificar el día"],
                "answer": 1,
                "explanation": "La rumiación es un factor de riesgo para depresión y ansiedad."
            },
            {
                "question": "¿Qué papel tiene el ejercicio en el manejo del estrés?",
                "options": ["Aumenta el estrés", "Libera endorfinas y reduce la tensión", "No tiene efecto", "Solo sirve si es muy intenso"],
                "answer": 1,
                "explanation": "El ejercicio moderado reduce la ansiedad y mejora el estado de ánimo."
            },
            {
                "question": "¿Qué es la fatiga adrenal? (concepto popular del estrés crónico)",
                "options": ["Enfermedad reconocida", "Sensación de agotamiento por estrés prolongado", "Aumento de energía", "Problema solo muscular"],
                "answer": 1,
                "explanation": "Aunque no es un diagnóstico médico aceptado, describe cansancio extremo y dificultad para manejar estrés."
            },
            {
                "question": "¿Cuál es una estrategia conductual para manejar el estrés?",
                "options": ["Evitar cualquier actividad", "Establecer límites y priorizar tareas", "Trabajar sin descansos", "Consumir alcohol"],
                "answer": 1,
                "explanation": "La gestión del tiempo y decir 'no' reduce la sobrecarga."
            }
        ],
        "Inteligencia Emocional": [
            {
                "question": "¿Qué es la inteligencia emocional?",
                "options": ["Capacidad de memorizar", "Reconocer, comprender y gestionar emociones propias y ajenas", "Tener un CI alto", "Evitar conflictos"],
                "answer": 1,
                "explanation": "Popularizada por Goleman, incluye autoconciencia, autorregulación, empatía y habilidades sociales."
            },
            {
                "question": "¿Qué componente de la inteligencia emocional implica reconocer las propias emociones?",
                "options": ["Autorregulación", "Autoconciencia emocional", "Empatía", "Habilidades sociales"],
                "answer": 1,
                "explanation": "Autoconciencia es la base para gestionar las emociones."
            },
            {
                "question": "¿Qué es la empatía?",
                "options": ["Sentir lástima", "Ponerse en el lugar del otro comprendiendo sus emociones", "Manipular emociones", "Indiferencia"],
                "answer": 1,
                "explanation": "La empatía cognitiva y afectiva mejora las relaciones interpersonales."
            },
            {
                "question": "¿Cuál es un indicador de baja inteligencia emocional?",
                "options": ["Hablar de sentimientos", "Reacciones explosivas sin reflexión", "Pedir retroalimentación", "Escuchar activamente"],
                "answer": 1,
                "explanation": "La impulsividad emocional sugiere dificultad en la autorregulación."
            },
            {
                "question": "¿Qué técnica ayuda a regular emociones intensas?",
                "options": ["Reaccionar inmediatamente", "Respirar profundamente y contar hasta 10", "Gritar", "Suprimir la emoción"],
                "answer": 1,
                "explanation": "El tiempo de pausa permite que la amígdala se calme y la corteza prefrontal tome el control."
            },
            {
                "question": "¿Qué habilidad social está asociada a la inteligencia emocional?",
                "options": ["Imponer la opinión", "Escucha activa y asertividad", "Aislamiento", "Competitividad extrema"],
                "answer": 1,
                "explanation": "La escucha activa y la asertividad mejoran la comunicación y la resolución de conflictos."
            },
            {
                "question": "¿Cuál es un beneficio de la inteligencia emocional en el trabajo?",
                "options": ["Mayor conflicto", "Mejor trabajo en equipo y liderazgo", "Menor productividad", "Aislamiento"],
                "answer": 1,
                "explanation": "Personas con alta IE manejan mejor el estrés y colaboran eficazmente."
            },
            {
                "question": "¿Qué es el 'labeling' de emociones?",
                "options": ["Ignorar la emoción", "Poner nombre a la emoción que se siente", "Exagerar la emoción", "Actuar sin pensar"],
                "answer": 1,
                "explanation": "Nombrar la emoción reduce su intensidad (efecto de etiquetado)."
            },
            {
                "question": "¿Qué es la resiliencia emocional?",
                "options": ["Nunca sentir emociones negativas", "Capacidad de adaptarse y recuperarse de la adversidad", "Ser insensible", "Evitar problemas"],
                "answer": 1,
                "explanation": "La resiliencia se puede desarrollar con estrategias de afrontamiento positivas."
            },
            {
                "question": "¿Cuál es una estrategia para mejorar la empatía?",
                "options": ["Juzgar a los demás", "Practicar la escucha activa sin interrumpir", "Hablar solo de uno mismo", "Evitar el contacto visual"],
                "answer": 1,
                "explanation": "La escucha activa muestra interés y comprensión hacia la otra persona."
            }
        ],
        "Sueño y Descanso": [
            {
                "question": "¿Cuántos ciclos de sueño completos se recomiendan por noche?",
                "options": ["1-2", "4-6", "7-8", "más de 10"],
                "answer": 1,
                "explanation": "Cada ciclo dura 90-110 minutos; 4-6 ciclos suman 7-9 horas."
            },
            {
                "question": "¿Qué fase del sueño es esencial para la consolidación de la memoria?",
                "options": ["Sueño ligero (N1)", "Ondas lentas (N3)", "REM (movimiento ocular rápido)", "Microdespertares"],
                "answer": 2,
                "explanation": "El sueño REM procesa emociones y fija memorias declarativas."
            },
            {
                "question": "¿Qué hormona regula el ritmo circadiano?",
                "options": ["Cortisol", "Melatonina", "Adrenalina", "Insulina"],
                "answer": 1,
                "explanation": "La melatonina se segrega en la oscuridad e induce el sueño."
            },
            {
                "question": "¿Cuál es un hábito de higiene del sueño recomendado?",
                "options": ["Usar pantallas brillantes antes de dormir", "Mantener horarios regulares", "Cenar muy pesado", "Hacer ejercicio intenso justo antes de acostarse"],
                "answer": 1,
                "explanation": "La regularidad ayuda a sincronizar el reloj biológico."
            },
            {
                "question": "¿Qué efecto tiene la cafeína en el sueño?",
                "options": ["Mejora la calidad", "Bloquea los receptores de adenosina, retrasando el sueño", "No tiene efecto", "Aumenta la melatonina"],
                "answer": 1,
                "explanation": "La vida media de la cafeína es de 4-6 horas, por lo que consumirla por la tarde afecta el sueño."
            },
            {
                "question": "¿Qué es la apnea obstructiva del sueño?",
                "options": ["Pesadillas frecuentes", "Pausas en la respiración durante el sueño", "Insomnio de conciliación", "Somnolencia excesiva diurna sin causa"],
                "answer": 1,
                "explanation": "Se asocia a ronquidos fuertes y fragmentación del sueño, con riesgo cardiovascular."
            },
            {
                "question": "¿Cuál es una consecuencia de la privación crónica del sueño?",
                "options": ["Mejor respuesta inmune", "Aumento de peso y riesgo de diabetes", "Mayor capacidad de concentración", "Reducción del estrés"],
                "answer": 1,
                "explanation": "La falta de sueño altera la leptina y grelina y reduce la sensibilidad a la insulina."
            },
            {
                "question": "¿Qué es la microsiesta (power nap)?",
                "options": ["Dormir más de 2 horas", "Siesta corta de 10-20 minutos", "Dormir de pie", "No dormir"],
                "answer": 1,
                "explanation": "La microsiesta mejora el estado de alerta sin causar inercia del sueño."
            },
            {
                "question": "¿Qué temperatura ambiente favorece el sueño?",
                "options": ["Muy caliente (>26°C)", "Fresca (18-22°C)", "Muy fría (<10°C)", "Indiferente"],
                "answer": 1,
                "explanation": "La temperatura fresca ayuda a disminuir la temperatura corporal central para dormir."
            },
            {
                "question": "¿Qué trastorno del sueño se caracteriza por movimientos involuntarios de las piernas?",
                "options": ["Narcolepsia", "Síndrome de piernas inquietas", "Terrores nocturnos", "Somnambulismo"],
                "answer": 1,
                "explanation": "El síndrome de piernas inquietas produce una necesidad irresistible de mover las piernas en reposo."
            }
        ],
        "Relaciones Sociales y Apoyo": [
            {
                "question": "¿Cómo afecta el aislamiento social a la salud mental?",
                "options": ["Mejora la autoestima", "Aumenta el riesgo de depresión y ansiedad", "No tiene efecto", "Aumenta la productividad"],
                "answer": 1,
                "explanation": "El apoyo social es un factor protector contra trastornos mentales."
            },
            {
                "question": "¿Qué es el ‘contagio emocional’?",
                "options": ["Enfermedad viral", "Tendencia a imitar y sincronizar emociones con otros", "Terapia grupal", "Aislamiento"],
                "answer": 1,
                "explanation": "Las emociones se transmiten a través de la imitación facial y la sincronía."
            },
            {
                "question": "¿Cuál es un beneficio de tener amistades cercanas?",
                "options": ["Mayor estrés", "Menor longevidad", "Mejor salud cardiovascular y mayor longevidad", "Aumento de la presión arterial"],
                "answer": 2,
                "explanation": "Estudios muestran que las relaciones sociales reducen la mortalidad."
            },
            {
                "question": "¿Qué comunicación es más efectiva en conflictos?",
                "options": ["Agresiva", "Pasiva", "Asertiva", "Sarcástica"],
                "answer": 2,
                "explanation": "La asertividad expresa necesidades respetando a los demás."
            },
            {
                "question": "¿Qué es la validación emocional?",
                "options": ["Ignorar la emoción", "Reconocer y aceptar la emoción del otro como comprensible", "Criticar la emoción", "Minimizarla"],
                "answer": 1,
                "explanation": "Validar no significa estar de acuerdo, sino mostrar comprensión empática."
            },
            {
                "question": "¿Cómo afecta el uso excesivo de redes sociales a las relaciones?",
                "options": ["Mejora la comunicación real", "Puede aumentar la comparación social y la soledad", "No tiene impacto", "Siempre es positivo"],
                "answer": 1,
                "explanation": "El uso pasivo (mirar sin interactuar) se asocia a menor bienestar."
            },
            {
                "question": "¿Qué es la escucha activa?",
                "options": ["Esperar el turno para hablar", "Prestar atención, parafrasear y hacer preguntas abiertas", "Interrumpir constantemente", "Dar consejos sin escuchar"],
                "answer": 1,
                "explanation": "Mejora la comprensión y fortalece la relación."
            },
            {
                "question": "¿Cuál es la diferencia entre apoyo social instrumental y emocional?",
                "options": ["No hay diferencia", "Instrumental es ayuda práctica (dinero, tareas), emocional es afecto y comprensión", "Emocional es más importante", "Instrumental es el único que importa"],
                "answer": 1,
                "explanation": "Ambos tipos de apoyo son importantes según la situación."
            },
            {
                "question": "¿Qué porcentaje de la comunicación es no verbal según estudios clásicos?",
                "options": ["10%", "30%", "55%", "80%"],
                "answer": 2,
                "explanation": "El lenguaje corporal y el tono de voz transmiten más que las palabras."
            },
            {
                "question": "¿Qué factor contribuye a la soledad no deseada en adultos mayores?",
                "options": ["Buena salud", "Pérdida de cónyuge y amigos, jubilación", "Actividades sociales frecuentes", "Vivir acompañado"],
                "answer": 1,
                "explanation": "Las transiciones vitales pueden reducir la red social."
            }
        ],
        "Técnicas de Relajación y Meditación": [
            {
                "question": "¿Qué es la meditación de atención enfocada?",
                "options": ["Concentrarse en un solo objeto, como la respiración", "Dejar la mente en blanco sin control", "Repetir mantras en voz alta", "Visualizar imágenes tranquilas"],
                "answer": 0,
                "explanation": "Entrena la atención sostenida y la conciencia de las distracciones."
            },
            {
                "question": "¿Cuántos minutos diarios de meditación muestran beneficios significativos?",
                "options": ["1 minuto", "10-20 minutos", "2 horas", "No hay evidencia"],
                "answer": 1,
                "explanation": "Estudios muestran cambios cerebrales positivos con práctica regular de 10-20 min."
            },
            {
                "question": "¿Qué es la relajación muscular progresiva de Jacobson?",
                "options": ["Tensar y relajar grupos musculares secuencialmente", "Masaje profundo", "Estiramientos pasivos", "Autohipnosis"],
                "answer": 0,
                "explanation": "Reduce la ansiedad al tomar conciencia de la tensión y liberarla."
            },
            {
                "question": "¿Qué es el biofeedback?",
                "options": ["Retroalimentación biológica mediante sensores para controlar funciones fisiológicas", "Un tipo de meditación", "Un fármaco", "Ejercicio aeróbico"],
                "answer": 0,
                "explanation": "Ayuda a aprender a regular la frecuencia cardíaca, tensión muscular, etc."
            },
            {
                "question": "¿Qué efecto tiene la meditación en la estructura cerebral?",
                "options": ["Ninguno", "Aumento de la densidad de materia gris en regiones relacionadas con la atención y regulación emocional", "Disminución del hipocampo", "Encogimiento cerebral"],
                "answer": 1,
                "explanation": "La neuroplasticidad permite cambios beneficiosos con la práctica."
            },
            {
                "question": "¿Qué es un mantra en la meditación?",
                "options": ["Postura corporal", "Sonido, palabra o frase repetida para enfocar la mente", "Respiración profunda", "Un tapete de meditación"],
                "answer": 1,
                "explanation": "El mantra ayuda a mantener la concentración y puede inducir un estado de calma."
            },
            {
                "question": "¿Cuál es la postura básica para meditar?",
                "options": ["Acostado plano", "Sentado con la espalda recta y cómodo", "De pie con brazos cruzados", "Caminando rápido"],
                "answer": 1,
                "explanation": "La columna recta facilita la respiración y la alerta relajada."
            },
            {
                "question": "¿Qué es el escaneo corporal (body scan)?",
                "options": ["Examen médico", "Técnica de mindfulness que dirige la atención a diferentes partes del cuerpo", "Un tipo de masaje", "Ejercicio de fuerza"],
                "answer": 1,
                "explanation": "Ayuda a soltar tensiones y conectarse con las sensaciones físicas."
            },
            {
                "question": "¿Qué es la meditación trascendental?",
                "options": ["Meditación con mantra personalizado, 20 min dos veces al día", "Técnica de respiración rápida", "Meditación caminando", "Yoga intenso"],
                "answer": 0,
                "explanation": "Popularizada por Maharishi Mahesh Yogi, busca trascender el pensamiento."
            },
            {
                "question": "¿Qué beneficio cardiovascular tiene la meditación regular?",
                "options": ["Aumenta la presión arterial", "Puede reducir la presión arterial y la frecuencia cardíaca", "No afecta", "Aumenta la arritmia"],
                "answer": 1,
                "explanation": "Reduce la actividad simpática y mejora la variabilidad cardíaca."
            }
        ]
    },
    "Higiene y Prevención de Enfermedades": {
        "Higiene Personal": [
            {
                "question": "¿Cuál es la técnica correcta para lavarse las manos?",
                "options": ["Solo agua", "Agua y jabón frotando al menos 20 segundos", "Solo alcohol en gel", "Secado al aire sin toalla"],
                "answer": 1,
                "explanation": "El frotado mecánico con jabón elimina gérmenes."
            },
            {
                "question": "¿Con qué frecuencia se debe cambiar el cepillo de dientes?",
                "options": ["Cada mes", "Cada 3-4 meses o cuando las cerdas estén desgastadas", "Cada año", "Solo cuando se enferma"],
                "answer": 1,
                "explanation": "Cepillos desgastados limpian menos y acumulan bacterias."
            },
            {
                "question": "¿Qué hábito de higiene previene infecciones de orina en mujeres?",
                "options": ["Limpieza de atrás hacia adelante", "Limpieza de adelante hacia atrás", "Uso de duchas vaginales", "Usar ropa interior sintética"],
                "answer": 1,
                "explanation": "Evita el arrastre de bacterias del ano hacia la uretra."
            },
            {
                "question": "¿Cada cuánto se recomienda bañarse?",
                "options": ["Varias veces al día", "Diario o día por medio según actividad", "Una vez por semana", "Solo cuando se es visible la suciedad"],
                "answer": 1,
                "explanation": "Baños diarios eliminan sudor y células muertas sin dañar la piel."
            },
            {
                "question": "¿Qué es la higiene de manos basada en alcohol en gel?",
                "options": ["Alternativa efectiva cuando no hay agua y jabón", "Mejor que lavar con agua y jabón", "No es efectiva", "Solo para niños"],
                "answer": 0,
                "explanation": "El alcohol al 60-70% mata la mayoría de los microorganismos."
            },
            {
                "question": "¿Cómo se debe cortar las uñas para evitar encarnaduras?",
                "options": ["En línea curva muy corta", "Recto sin cortar las esquinas", "Muy profundas", "Con tijeras sin limar"],
                "answer": 1,
                "explanation": "Cortar recto previene que la uña crezca hacia la piel."
            },
            {
                "question": "¿Qué medida de higiene es clave para prevenir el pie de atleta?",
                "options": ["Usar zapatos de plástico", "Secar bien entre los dedos y usar calcetines de algodón", "Caminar descalzo en duchas públicas", "Usar el mismo calzado siempre"],
                "answer": 1,
                "explanation": "La humedad favorece los hongos; mantener los pies secos es esencial."
            },
            {
                "question": "¿Qué es la higiene del sueño?",
                "options": ["Dormir más horas", "Conjunto de prácticas para mejorar la calidad del sueño", "Usar pijama nuevo", "Beber café antes de dormir"],
                "answer": 1,
                "explanation": "Incluye rutinas, ambiente oscuro y evitar pantallas."
            },
            {
                "question": "¿Con qué frecuencia se deben cambiar las sábanas?",
                "options": ["Cada día", "Cada 1-2 semanas", "Cada 3 meses", "Una vez al año"],
                "answer": 1,
                "explanation": "Se acumulan células muertas, ácaros y bacterias."
            },
            {
                "question": "¿Qué es el corte seguro de uñas en personas diabéticas?",
                "options": ["Cortar muy corto", "Limado suave y evitar esquinas cortantes, por profesional si es necesario", "Usar cortaúñas sin cuidado", "No cortarlas nunca"],
                "answer": 1,
                "explanation": "Los diabéticos tienen riesgo de infecciones por heridas pequeñas."
            }
        ],
        "Enfermedades Infecciosas": [
            {
                "question": "¿Qué es la cadena de transmisión de una infección?",
                "options": ["Tratamiento con antibióticos", "Secuencia: agente, reservorio, puerta de salida, transmisión, puerta de entrada, huésped susceptible", "Síntomas de la enfermedad", "Inmunidad de rebaño"],
                "answer": 1,
                "explanation": "Interrumpir cualquier eslabón previene la infección."
            },
            {
                "question": "¿Cuál es la principal vía de transmisión de la gripe?",
                "options": ["Alimentos contaminados", "Gotitas respiratorias (toser, estornudar)", "Agua", "Picadura de mosquito"],
                "answer": 1,
                "explanation": "El virus influenza se propaga por aerosoles y contacto con superficies."
            },
            {
                "question": "¿Qué es la inmunidad de rebaño?",
                "options": ["Vacunación obligatoria", "Protección indirecta cuando un alto porcentaje de la población es inmune", "Aislamiento total", "Uso de mascarillas"],
                "answer": 1,
                "explanation": "Reduce la propagación protegiendo a los vulnerables."
            },
            {
                "question": "¿Qué enfermedad se previene con la vacuna BCG?",
                "options": ["Tétanos", "Tuberculosis (formas graves)", "Polio", "Hepatitis B"],
                "answer": 1,
                "explanation": "BCG protege contra la tuberculosis diseminada en niños."
            },
            {
                "question": "¿Cuál es una medida efectiva contra la transmisión de COVID-19?",
                "options": ["Usar mascarilla en espacios concurridos", "Tocar superficies", "No ventilar habitaciones", "Ignorar los síntomas"],
                "answer": 0,
                "explanation": "Las mascarillas reducen la emisión y exposición a gotitas respiratorias."
            },
            {
                "question": "¿Qué es un antibiótico?",
                "options": ["Antiviral", "Medicamento que mata bacterias o inhibe su crecimiento", "Analgésico", "Antiinflamatorio"],
                "answer": 1,
                "explanation": "No funcionan contra virus, solo bacterias."
            },
            {
                "question": "¿Qué es la resistencia a los antibióticos?",
                "options": ["Alergia a antibióticos", "Capacidad de las bacterias de sobrevivir a los antibióticos", "Efecto secundario", "Dosis insuficiente"],
                "answer": 1,
                "explanation": "Causada por uso inadecuado; es un grave problema de salud pública."
            },
            {
                "question": "¿Cómo se transmite el VIH?",
                "options": ["Por saliva o abrazos", "Relaciones sexuales sin protección, sangre, madre a hijo", "Aire", "Picadura de insecto"],
                "answer": 1,
                "explanation": "No se transmite por contacto casual."
            },
            {
                "question": "¿Qué es la cuarentena?",
                "options": ["Aislamiento de personas expuestas a una enfermedad contagiosa", "Tratamiento hospitalario", "Vacunación masiva", "Cierre de fronteras"],
                "answer": 0,
                "explanation": "Evita la propagación durante el período de incubación."
            },
            {
                "question": "¿Qué es el lavado de manos quirúrgico?",
                "options": ["Enjuague rápido", "Lavado profundo con cepillo y antiséptico, hasta los codos", "Usar solo alcohol", "No secarse"],
                "answer": 1,
                "explanation": "Elimina la flora transitoria y reduce la permanente."
            }
        ],
        "Vacunación": [
            {
                "question": "¿Qué es la vacunación?",
                "options": ["Administración de un medicamento para curar", "Administración de un antígeno para estimular la inmunidad", "Una cirugía", "Un tipo de antibiótico"],
                "answer": 1,
                "explanation": "Las vacunas preparan al sistema inmunitario para futuras infecciones."
            },
            {
                "question": "¿Qué vacuna se administra al nacer en muchos países?",
                "options": ["Sarampión", "BCG y Hepatitis B", "Varicela", "VPH"],
                "answer": 1,
                "explanation": "La BCG protege contra TB y la hepatitis B contra el virus."
            },
            {
                "question": "¿Qué es la vacuna de la gripe?",
                "options": ["Protege contra todos los virus respiratorios", "Protege contra las cepas de influenza más probables cada año", "Es una antitoxina", "Se toma por vía oral"],
                "answer": 1,
                "explanation": "Debido a mutaciones, se reformula anualmente."
            },
            {
                "question": "¿Qué es la vacuna HPV?",
                "options": ["Hepatitis", "Virus del papiloma humano, previene cáncer cervicouterino", "Herpes", "VIH"],
                "answer": 1,
                "explanation": "Recomendada en adolescentes antes del inicio de la actividad sexual."
            },
            {
                "question": "¿Qué significa que una vacuna es inactivada?",
                "options": ["Contiene virus vivos atenuados", "Contiene virus muertos o fragmentados", "Es de ARN mensajero", "Es una toxoide"],
                "answer": 1,
                "explanation": "No pueden causar enfermedad, pero a menudo requieren dosis de refuerzo."
            },
            {
                "question": "¿Qué es la vacuna de ARNm?",
                "options": ["Contiene virus atenuado", "Instrucciones para que las células produzcan una proteína viral", "Anticuerpos preformados", "Un tipo de antibiótico"],
                "answer": 1,
                "explanation": "Tecnología usada en algunas vacunas contra COVID-19."
            },
            {
                "question": "¿Por qué es importante la vacunación infantil?",
                "options": ["Porque los niños tienen sistema inmune débil y pueden sufrir enfermedades graves", "No es necesaria", "Solo para viajes", "Para evitar la escuela"],
                "answer": 0,
                "explanation": "Previene muertes y discapacidades por enfermedades prevenibles."
            },
            {
                "question": "¿Qué es un refuerzo (dosis booster)?",
                "options": ["Dosis adicional para mantener la inmunidad", "Primera dosis", "Reacción alérgica", "Vacuna de emergencia"],
                "answer": 0,
                "explanation": "Necesario cuando la memoria inmunológica disminuye con el tiempo."
            },
            {
                "question": "¿Cuánto tiempo tarda en desarrollarse la inmunidad después de una vacuna?",
                "options": ["Horas", "1-2 semanas aproximadamente", "Inmediatamente", "6 meses"],
                "answer": 1,
                "explanation": "El cuerpo necesita tiempo para producir anticuerpos y células de memoria."
            },
            {
                "question": "¿Qué es la vacuna DTP?",
                "options": ["Difteria, tétanos, tos ferina", "Dengue, tifus, polio", "Difteria, tuberculosis, paperas", "Difteria, tétanos, parotiditis"],
                "answer": 0,
                "explanation": "Común en el calendario infantil."
            }
        ],
        "Salud Bucal": [
            {
                "question": "¿Cuál es la principal causa de caries dental?",
                "options": ["Cepillado agresivo", "Azúcares y bacterias que producen ácido", "Falta de flúor", "Genética"],
                "answer": 1,
                "explanation": "Las bacterias fermentan azúcares, desmineralizando el esmalte."
            },
            {
                "question": "¿Cada cuánto se recomienda la revisión dental?",
                "options": ["Cada mes", "Cada 6-12 meses", "Cada 5 años", "Solo cuando duele"],
                "answer": 1,
                "explanation": "Las revisiones periódicas detectan problemas tempranos."
            },
            {
                "question": "¿Qué hace el flúor en los dientes?",
                "options": ["Daña el esmalte", "Remineraliza y fortalece el esmalte contra ácidos", "Blanquea los dientes", "Elimina la placa"],
                "answer": 1,
                "explanation": "Forma fluorapatita, más resistente a los ácidos."
            },
            {
                "question": "¿Qué enfermedad gingival se caracteriza por inflamación reversible?",
                "options": ["Periodontitis", "Gingivitis", "Caries", "Absceso"],
                "answer": 1,
                "explanation": "La gingivitis es inflamación de las encías sin pérdida de hueso."
            },
            {
                "question": "¿Cuál es la técnica correcta de cepillado?",
                "options": ["Movimientos horizontales agresivos", "Cepillo en ángulo de 45 grados, movimientos suaves y cortos", "Solo enjuague", "Cepillar muy rápido"],
                "answer": 1,
                "explanation": "Limpia el surco gingival sin dañar encías."
            },
            {
                "question": "¿Con qué frecuencia se debe usar el hilo dental?",
                "options": ["Una vez a la semana", "Una vez al día, preferiblemente antes del cepillado", "Solo cuando hay comida atascada", "No es necesario"],
                "answer": 1,
                "explanation": "Elimina placa entre dientes donde el cepillo no alcanza."
            },
            {
                "question": "¿Qué es el sarro dental?",
                "options": ["Caries avanzada", "Placa bacteriana mineralizada (cálculo)", "Gingivitis", "Fractura dental"],
                "answer": 1,
                "explanation": "Solo puede ser removido por un profesional."
            },
            {
                "question": "¿Qué alimentos ayudan a limpiar los dientes de forma natural?",
                "options": ["Caramelos pegajosos", "Manzanas y zanahorias crudas", "Refrescos", "Galletas dulces"],
                "answer": 1,
                "explanation": "Estimulan la saliva y remueven residuos mecánicamente."
            },
            {
                "question": "¿Qué es la sensibilidad dental?",
                "options": ["Dolor al cepillarse", "Dolor agudo ante estímulos fríos, calientes o dulces", "Dolor al masticar", "Sangrado de encías"],
                "answer": 1,
                "explanation": "Por exposición de dentina o recesión gingival."
            },
            {
                "question": "¿Cuál es un signo de periodontitis?",
                "options": ["Encías rosadas firmes", "Retracción de encías, movilidad dental y mal aliento", "Dientes blancos", "Sin sangrado al cepillarse"],
                "answer": 1,
                "explanation": "La periodontitis es una infección grave que destruye el hueso."
            }
        ],
        "Prevención de Enfermedades Crónicas": [
            {
                "question": "¿Qué factor de riesgo para enfermedades cardiovasculares es modificable?",
                "options": ["Edad", "Genética", "Tabaquismo y sedentarismo", "Sexo"],
                "answer": 2,
                "explanation": "Dejar de fumar y hacer ejercicio reducen significativamente el riesgo."
            },
            {
                "question": "¿Qué valores de presión arterial se consideran hipertensión?",
                "options": ["<120/80", "≥140/90 mmHg", "100/60", "130/85"],
                "answer": 1,
                "explanation": "La hipertensión es un factor de riesgo silencioso."
            },
            {
                "question": "¿Qué es la diabetes tipo 2?",
                "options": ["Enfermedad autoinmune", "Resistencia a la insulina y déficit relativo", "Falta total de insulina", "Enfermedad renal"],
                "answer": 1,
                "explanation": "Asociada a obesidad y sedentarismo; prevenible con estilo de vida."
            },
            {
                "question": "¿Cuál es la principal causa de cáncer de pulmón?",
                "options": ["Contaminación ambiental", "Tabaquismo (activo o pasivo)", "Genética", "Radón"],
                "answer": 1,
                "explanation": "El tabaco causa aproximadamente el 85% de los casos."
            },
            {
                "question": "¿Qué es el colesterol LDL?",
                "options": ["Colesterol 'bueno'", "Colesterol 'malo' que contribuye a aterosclerosis", "Triglicéridos", "Lipoproteína de alta densidad"],
                "answer": 1,
                "explanation": "Mantenerlo bajo reduce el riesgo cardiovascular."
            },
            {
                "question": "¿Qué prueba de tamizaje detecta temprano el cáncer de mama?",
                "options": ["Papanicolaou", "Mamografía", "Colonoscopía", "PSA"],
                "answer": 1,
                "explanation": "Se recomienda cada 1-2 años a partir de los 40-50 años."
            },
            {
                "question": "¿Qué es la osteoporosis?",
                "options": ["Artritis", "Pérdida de densidad ósea con riesgo de fracturas", "Debilidad muscular", "Problema de coagulación"],
                "answer": 1,
                "explanation": "Prevenible con calcio, vitamina D y ejercicio de impacto."
            },
            {
                "question": "¿Qué es el síndrome metabólico?",
                "options": ["Conjunto de afecciones: obesidad abdominal, hipertensión, glucosa alta, dislipidemia", "Enfermedad renal", "Trastorno mental", "Infección viral"],
                "answer": 0,
                "explanation": "Aumenta el riesgo de diabetes y enfermedades del corazón."
            },
            {
                "question": "¿Qué porcentaje de casos de cáncer colorrectal se puede prevenir con hábitos saludables?",
                "options": ["5%", "20%", "50% o más", "0%"],
                "answer": 2,
                "explanation": "Dieta rica en fibra, ejercicio y evitar carnes procesadas reduce el riesgo."
            },
            {
                "question": "¿Qué es la EPOC (Enfermedad Pulmonar Obstructiva Crónica)?",
                "options": ["Asma", "Obstrucción crónica del flujo aéreo, generalmente por tabaco", "Fibrosis pulmonar", "Neumonía recurrente"],
                "answer": 1,
                "explanation": "Principal causa evitable: tabaquismo."
            }
        ]
    },
    "Primeros Auxilios y Respuesta a Emergencias": {
        "RCP Básico y DEA": [
            {
                "question": "¿Cuál es la secuencia del RCP básico en adultos según guías recientes?",
                "options": ["A-B-C (vía aérea, respiración, compresiones)", "C-A-B (compresiones, vía aérea, respiración)", "B-C-A", "Solo compresiones"],
                "answer": 1,
                "explanation": "Priorizar compresiones aumenta la supervivencia al mantener la perfusión cerebral."
            },
            {
                "question": "¿A qué ritmo se deben realizar las compresiones torácicas?",
                "options": ["60-80 por minuto", "100-120 por minuto", "140-160 por minuto", "Lo más rápido posible"],
                "answer": 1,
                "explanation": "Un ritmo de 100-120 compresiones por minuto (al ritmo de 'Stayin' Alive')."
            },
            {
                "question": "¿Qué profundidad de compresión se recomienda en adultos?",
                "options": ["2-3 cm", "5-6 cm", "7-8 cm", "10 cm"],
                "answer": 1,
                "explanation": "Al menos 5 cm y no más de 6 cm para permitir el retroceso completo del tórax."
            },
            {
                "question": "¿Qué relación compresión-ventilación se usa en RCP para adultos con un solo reanimador?",
                "options": ["30:2", "15:2", "5:1", "Solo compresiones"],
                "answer": 0,
                "explanation": "30 compresiones seguidas de 2 ventilaciones."
            },
            {
                "question": "¿Qué es un DEA (desfibrilador externo automático)?",
                "options": ["Equipo que analiza el ritmo cardíaco y puede administrar una descarga", "Medicamento intravenoso", "Ventilador mecánico", "Monitor de presión arterial"],
                "answer": 0,
                "explanation": "Su uso temprano en paro por fibrilación ventricular salva vidas."
            },
            {
                "question": "¿Cuándo se debe colocar el DEA?",
                "options": ["Inmediatamente después de llamar al 911, si está disponible", "Después de 10 minutos de RCP", "Solo si la víctima recupera el pulso", "Antes de verificar la respiración"],
                "answer": 0,
                "explanation": "Cada minuto sin desfibrilación reduce la supervivencia un 7-10%."
            },
            {
                "question": "¿Qué hacer si la víctima tiene un desfibrilador implantable y está en paro?",
                "options": ["No hacer nada", "Realizar RCP normalmente; el DEA externo no interfiere", "Desconectar el implante", "Evitar compresiones"],
                "answer": 1,
                "explanation": "Los parches del DEA se colocan evitando el dispositivo interno."
            },
            {
                "question": "¿Cuándo se debe detener la RCP?",
                "options": ["Después de 5 minutos", "Cuando la víctima recupere signos de vida o llegue ayuda avanzada", "Cuando esté cansado", "Si no hay DEA"],
                "answer": 1,
                "explanation": "Continuar hasta que el personal médico relevo o la víctima responda."
            },
            {
                "question": "¿Qué hacer si la víctima vomita durante la RCP?",
                "options": ["Detener la RCP", "Girar la cabeza hacia un lado, limpiar el vómito y continuar", "Aumentar la profundidad de compresiones", "Dar ventilaciones más fuertes"],
                "answer": 1,
                "explanation": "Evitar aspiración; luego reanudar compresiones."
            },
            {
                "question": "¿Qué ritmo cardíaco es 'desfibrilable'?",
                "options": ["Asistolia", "Fibrilación ventricular o taquicardia ventricular sin pulso", "Bradicardia sinusal", "Ritmo sinusal normal"],
                "answer": 1,
                "explanation": "El DEA solo descarga en ritmos desfibrilables."
            }
        ],
        "Hemorragias y Heridas": [
            {
                "question": "¿Cuál es la primera acción ante una hemorragia externa grave?",
                "options": ["Aplicar un torniquete", "Presión directa con un apósito", "Limpiar la herida con alcohol", "Elevar la extremidad"],
                "answer": 1,
                "explanation": "La presión directa es lo más efectivo para controlar la mayoría de hemorragias."
            },
            {
                "question": "¿Cuándo se debe aplicar un torniquete?",
                "options": ["Siempre en cualquier herida", "Cuando la presión directa no controla la hemorragia que amenaza la vida", "En heridas leves", "Para cualquier sangrado nasal"],
                "answer": 1,
                "explanation": "El torniquete es una medida salvadora pero debe usarse solo en casos extremos."
            },
            {
                "question": "¿Cuál es la ubicación correcta del torniquete?",
                "options": ["Sobre la herida", "Encima de la herida, entre 5-7 cm proximal", "Debajo de la herida", "En la articulación"],
                "answer": 1,
                "explanation": "Lo más cerca posible de la herida, pero no sobre ella."
            },
            {
                "question": "¿Qué hacer ante una hemorragia nasal (epistaxis)?",
                "options": ["Inclinar la cabeza hacia atrás", "Inclinar la cabeza hacia adelante y presionar la fosa nasal sangrante por 10-15 minutos", "Tapar la nariz con algodón", "Acostar a la persona"],
                "answer": 1,
                "explanation": "Inclinar hacia adelante evita la deglución de sangre."
            },
            {
                "question": "¿Cómo se limpia una herida menor?",
                "options": ["Con alcohol puro", "Con agua y jabón suave, o suero fisiológico", "Con vinagre", "Con gasa seca"],
                "answer": 1,
                "explanation": "Elimina suciedad y reduce infección sin dañar tejido."
            },
            {
                "question": "¿Qué signo indica que una herida necesita sutura?",
                "options": ["Longitud menor de 1 cm", "Bordes separados, sangrado activo, localización en cara", "No sangra", "Es superficial"],
                "answer": 1,
                "explanation": "Heridas profundas o con pérdida de sustancia requieren valoración médica."
            },
            {
                "question": "¿Qué es un hematoma?",
                "options": ["Infección de la piel", "Acumulación de sangre bajo la piel tras un golpe", "Rotura de vaso superficial", "Quiste"],
                "answer": 1,
                "explanation": "Aplicar hielo reduce la inflamación y el dolor."
            },
            {
                "question": "¿Qué hacer ante una herida por mordedura de animal?",
                "options": ["Ignorar", "Limpiar, cubrir y acudir a urgencias por posible profilaxis antirrábica y antibióticos", "Aplicar pomada antibiótica y vendar", "Cauterizar"],
                "answer": 1,
                "explanation": "Riesgo de infección por Pasteurella, rabia, etc."
            },
            {
                "question": "¿Qué es un apósito hemostático?",
                "options": ["Gasa normal", "Material que acelera la coagulación para hemorragias graves", "Venda elástica", "Cinta adhesiva"],
                "answer": 1,
                "explanation": "Contiene agentes como caolín o quitosano."
            },
            {
                "question": "¿Qué hacer si un objeto está clavado en una herida?",
                "options": ["Retirarlo inmediatamente", "No retirarlo, inmovilizar y acudir al hospital", "Cortarlo al ras", "Aplicar hielo"],
                "answer": 1,
                "explanation": "Extraerlo podría causar más sangrado o daño."
            }
        ],
        "Quemaduras y Lesiones por Calor": [
            {
                "question": "¿Cuál es la primera medida para una quemadura térmica superficial?",
                "options": ["Aplicar hielo directamente", "Enfriar con agua corriente a 10-20°C durante al menos 10-20 minutos", "Aplicar mantequilla", "Romper las ampollas"],
                "answer": 1,
                "explanation": "El agua corriente detiene la progresión del daño térmico."
            },
            {
                "question": "¿Qué clasificación de quemadura afecta todas las capas de la piel?",
                "options": ["Primer grado", "Segundo grado", "Tercer grado", "Cuarto grado"],
                "answer": 2,
                "explanation": "Las de tercer grado son indoloras (destrucción nerviosa) y requieren injertos."
            },
            {
                "question": "¿Qué NO se debe aplicar en una quemadura?",
                "options": ["Agua fría", "Hielo, pasta dental, aceite o remedios caseros", "Gasas estériles", "Sueros"],
                "answer": 1,
                "explanation": "El hielo directo empeora la isquemia; otros productos contaminan."
            },
            {
                "question": "¿Qué es el golpe de calor?",
                "options": ["Insolación leve", "Temperatura corporal >40°C con alteración neurológica, emergencia médica", "Calambres por calor", "Deshidratación leve"],
                "answer": 1,
                "explanation": "Requiere enfriamiento rápido y atención urgente."
            },
            {
                "question": "¿Cómo se trata una quemadura química por ácido?",
                "options": ["Neutralizar con una base", "Lavar con abundante agua corriente durante al menos 20 minutos", "Aplicar alcohol", "Cubrir con vendaje seco"],
                "answer": 1,
                "explanation": "La irrigación copiosa diluye y elimina el químico; no neutralizar porque causa reacción exotérmica."
            },
            {
                "question": "¿Qué signo indica que una quemadura puede ser de segundo grado?",
                "options": ["Enrojecimiento", "Ampollas (flictenas) y dolor intenso", "Piel carbonizada", "Insensibilidad"],
                "answer": 1,
                "explanation": "La capa basal está dañada, formándose ampollas."
            },
            {
                "question": "¿Qué hacer ante una quemadura eléctrica?",
                "options": ["Tocar a la víctima sin precaución", "Desconectar la fuente o apartar con objeto no conductor", "Aplicar hielo", "Dar agua"],
                "answer": 1,
                "explanation": "La prioridad es la seguridad del reanimador; las lesiones internas pueden ser graves."
            },
            {
                "question": "¿Qué es la regla de los nueve para estimar área quemada?",
                "options": ["Método para calcular fluidos", "Método para estimar el porcentaje de superficie corporal quemada", "Regla de reanimación", "Escala de dolor"],
                "answer": 1,
                "explanation": "Asigna porcentajes a segmentos corporales (ej. cabeza 9%, cada brazo 9%, etc.)."
            },
            {
                "question": "¿Qué hacer si una ampolla se rompe?",
                "options": ["Dejar la piel suelta", "Limpiar suavemente, aplicar antibiótico tópico y cubrir con apósito no adherente", "No hacer nada", "Quitar toda la piel"],
                "answer": 1,
                "explanation": "Previene infección mientras cicatriza la piel nueva."
            },
            {
                "question": "¿Qué es la hipotermia?",
                "options": ["Temperatura corporal <35°C", "Fiebre alta", "Golpe de calor", "Deshidratación"],
                "answer": 0,
                "explanation": "Puede causar confusión, rigidez y paro cardíaco; requiere calentamiento pasivo o activo."
            }
        ],
        "Fracturas, Esguinces y Luxaciones": [
            {
                "question": "¿Cuál es la diferencia entre fractura y esguince?",
                "options": ["No hay diferencia", "Fractura es hueso, esguince es lesión de ligamento", "Esguince es músculo", "Fractura es cartílago"],
                "answer": 1,
                "explanation": "El esguince es una distensión o rotura de ligamentos."
            },
            {
                "question": "¿Qué signo es característico de una fractura?",
                "options": ["Hematoma leve", "Deformidad, crepitación, movimiento anormal", "Dolor solo a la palpación", "Hinchazón difusa"],
                "answer": 1,
                "explanation": "La crepitación (roce de huesos) es patognomónico pero no debe provocarse."
            },
            {
                "question": "¿Qué hacer ante una sospecha de fractura?",
                "options": ["Mover la extremidad para comprobar", "Inmovilizar la zona tal como está, aplicar hielo y acudir a urgencias", "Masajear", "Aplicar calor"],
                "answer": 1,
                "explanation": "La inmovilización evita daño adicional."
            },
            {
                "question": "¿Qué es una luxación?",
                "options": ["Fractura intraarticular", "Pérdida de contacto de las superficies articulares", "Esguince grave", "Rotura de tendón"],
                "answer": 1,
                "explanation": "Requiere reducción médica; no intentar reubicar por cuenta propia."
            },
            {
                "question": "¿Qué protocolo se usa para esguince agudo?",
                "options": ["Calor, movimiento activo", "RICE (Reposo, Hielo, Compresión, Elevación)", "Inmovilización rígida total", "Aplicar calor seco"],
                "answer": 1,
                "explanation": "Reduce inflamación y dolor en las primeras 48 horas."
            },
            {
                "question": "¿Cuánto tiempo aplicar hielo en una lesión aguda?",
                "options": ["5 minutos", "15-20 minutos cada 2-3 horas", "1 hora continua", "No aplicar hielo"],
                "answer": 1,
                "explanation": "Periodos cortos evitan lesión por frío, pero suficiente para vasoconstricción."
            },
            {
                "question": "¿Qué es una fractura abierta?",
                "options": ["Hueso roto sin herida", "Hueso que perfora la piel o hay herida comunicante", "Fractura múltiple", "Fractura intraarticular"],
                "answer": 1,
                "explanation": "Alto riesgo de infección; cubrir con apósito estéril, no recolocar el hueso."
            },
            {
                "question": "¿Qué inmovilización provisional se puede hacer en el campo?",
                "options": ["Férula improvisada con materiales rígidos (revista, cartón) acolchada", "Venda elástica muy apretada", "No inmovilizar", "Atar la extremidad al cuerpo"],
                "answer": 0,
                "explanation": "Acolchado evita más daño; inmovilizar articulaciones adyacentes."
            },
            {
                "question": "¿Qué es una fisura?",
                "options": ["Fractura completa", "Fractura incompleta (grieta sin desplazamiento)", "Esguince óseo", "Luxación"],
                "answer": 1,
                "explanation": "Suele tratarse con inmovilización, no quirúrgica."
            },
            {
                "question": "¿Qué signo NO debe estar presente en un esguince leve?",
                "options": ["Dolor", "Hinchazón leve", "Deformidad ósea", "Moretón"],
                "answer": 2,
                "explanation": "La deformidad sugiere fractura o luxación."
            }
        ],
        "Asfixia, Obstrucción y Ahogamiento": [
            {
                "question": "¿Qué hacer si un adulto se está ahogando y puede toser con fuerza?",
                "options": ["Aplicar maniobra de Heimlich", "Animar a toser y no interferir", "Dar golpes en la espalda", "Acostar a la persona"],
                "answer": 1,
                "explanation": "La tos efectiva puede expulsar el objeto; intervenir solo si empeora."
            },
            {
                "question": "¿Cuál es la maniobra para un adulto consciente con obstrucción completa de la vía aérea?",
                "options": ["Compresiones torácicas", "Maniobra de Heimlich (compresiones abdominales)", "Ventilaciones", "Pinzar la nariz"],
                "answer": 1,
                "explanation": "Se colocan los brazos alrededor del abdomen y se realiza una compresión hacia arriba."
            },
            {
                "question": "¿Qué hacer si la víctima por ahogamiento está inconsciente?",
                "options": ["Iniciar RCP inmediato, empezando por compresiones", "Intentar extraer agua de los pulmones", "Posición de seguridad", "Dar palmadas en la espalda"],
                "answer": 0,
                "explanation": "El RCP con compresiones es prioritario; las maniobras para expulsar agua retrasan la oxigenación."
            },
            {
                "question": "¿Cuántas compresiones abdominales se realizan en la maniobra de Heimlich?",
                "options": ["Hasta que el objeto salga o la víctima pierda la conciencia", "Solo 5", "10", "Continuar hasta 50"],
                "answer": 0,
                "explanation": "Se repiten sucesivamente hasta la efectividad o la pérdida de conciencia."
            },
            {
                "question": "¿Qué hacer si la víctima de obstrucción está embarazada u obesa?",
                "options": ["Compresiones abdominales igual", "Compresiones torácicas (en lugar de abdominales)", "Golpes en la espalda", "No hacer nada"],
                "answer": 1,
                "explanation": "Las compresiones torácicas evitan daño al útero y son efectivas."
            },
            {
                "question": "¿Qué hacer si la víctima pierde la conciencia durante la asfixia?",
                "options": ["Continuar Heimlich", "Iniciar RCP, revisar la boca antes de las ventilaciones", "Solo ventilaciones", "Colocar en posición lateral"],
                "answer": 1,
                "explanation": "Al abrir la vía aérea, si se ve el objeto, se extrae; luego RCP."
            },
            {
                "question": "¿Cuál es la causa más común de ahogamiento en niños pequeños?",
                "options": ["Piscinas profundas", "Inmersión en agua (bañeras, cubos) sin supervisión", "Tormentas", "Bebidas calientes"],
                "answer": 1,
                "explanation": "La supervisión constante es vital; los niños pueden ahogarse en pocos centímetros de agua."
            },
            {
                "question": "¿Qué es la respiración de rescate en el ahogamiento?",
                "options": ["Ventilaciones boca a boca", "Compresiones torácicas", "Maniobra de Heimlich", "Uso de DEA"],
                "answer": 0,
                "explanation": "Se administran 2 ventilaciones iniciales antes de comenzar compresiones en el ahogamiento."
            },
            {
                "question": "¿Cuál es un signo de obstrucción parcial de la vía aérea?",
                "options": ["Silencio absoluto", "Tos débil y ruidos estridentes", "Cianosis inmediata", "Respiración tranquila"],
                "answer": 1,
                "explanation": "La víctima puede emitir sonidos pero tiene dificultad para respirar."
            },
            {
                "question": "¿Qué hacer si se extrae un objeto de la boca durante RCP?",
                "options": ["Continuar RCP normal", "Revisar si hay respiración espontánea, si no, continuar RCP", "Dar agua", "Detener maniobras"],
                "answer": 1,
                "explanation": "Aún puede no haber retorno de circulación o respiración; seguir según evaluación."
            }
        ]
    }
}