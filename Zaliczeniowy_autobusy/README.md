# Опис рефакториизації

Цей розділ описує зміни, внесені до проекту на основі принципів об'єктно-орієнтованого програмування (ООП) та архітектурних патернів, що покращили структуру коду та покращили тестованість.

## 1. Інкапсуляція
**Покращено:**

Введення методів в окремі модулі дозволяє приховати деталі реалізації. Наприклад, обчислення відстані тепер здійснюється через методи в модулі `geo_utils` (зокрема, функція `haversine_distance`), що забезпечує кращу організацію та інкапсуляцію логіки обчислення географічних відстаней.

## 2. Патерн "Стратегія"
**Покращено:**

Для обчислення швидкості використано патерн "Стратегія". Зокрема, для вибору стратегії обчислення швидкості використовується клас `SpeedCalculationFactory`, який дозволяє змінювати алгоритм обчислення без змін в основному коді програми. Це дозволяє додавати нові стратегії для обчислення швидкості, як наприклад `HaversineSpeedCalculationStrategy`, без необхідності модифікації інших компонентів програми.

## 3. Розподіл функціональності
**Покращено:**

Код був розбитий на більш спеціалізовані функції в різних утилітних модулях: методи для обчислень відстаней тепер знаходяться в `geo_utils`, а методи для взаємодії з API — в `api_utils`. Це дозволяє зосередити кожен модуль на окремому завданні, знижуючи складність і покращуючи масштабованість проекту.

## 4. Простота (KISS - Keep It Simple, Stupid)
**Покращено:**

Логіка була спрощена завдяки виділенню окремих методів для специфічних завдань. Кожен метод тепер відповідає за одну функціональність, що робить код більш зрозумілим та простим для розуміння. Наприклад, функція `find_violations_places` відповідає лише за кластеризацію порушень швидкості, що полегшує підтримку та тестування.

## 5. Можливість розвитку (Open/Closed Principle)
**Покращено:**

Всі методи для обчислення швидкості та відстаней в `geo_utils` тепер підтримують додавання нових алгоритмів обчислення без зміни існуючого коду. Це дозволяє легко додавати нові стратегії, як, наприклад, інші алгоритми для обчислення відстані або нові стратегії для визначення швидкості, що значно підвищує можливість розвитку програми без порушення роботи існуючих компонентів.

## 6. Абстракція
**Покращено:**

Використання абстракцій для роботи з API в `api_utils` дозволяє приховати всі деталі реалізації HTTP-запитів та обробки відповідей. Це дає змогу змінювати API або тип запитів без змін у всьому коді. Наприклад, методи для взаємодії з API тепер зосереджені в одному модулі, що полегшує їх тестування та підтримку.

## 7. DRY (Don't Repeat Yourself)
**Покращено:**

Зменшено дублювання коду завдяки виділенню логіки в окремі функції та модулі. Логіка взаємодії з API та збереження результатів тепер обробляється окремими методами в `api_utils` та іншими утилітами, що робить код більш гнучким і зручним для масштабування.

## 8. SOLID (особливо принципи "Single Responsibility" і "Dependency Inversion")
**Покращено:**

- **Single Responsibility:** Кожен метод тепер має одну відповідальність. Наприклад, функції для обчислення відстаней знаходяться в модулі `geo_utils`, а логіка взаємодії з API — в `api_utils`. Це полегшує підтримку і тестування.
- **Dependency Inversion:** Використання патерну стратегій дозволяє програми залежати від абстракцій, а не від конкретних реалізацій. Наприклад, клас `SpeedViolationCheckerFactory` залежить від абстракції стратегії для обчислення швидкості, що дозволяє легко замінювати стратегії без зміни бізнес-логіки програми.

## 9. Підвищення тестованості
**Покращено:**

Розбиття коду на окремі методи та модулі значно полегшує написання юніт-тестів. Тестувати окремі частини програми стало набагато простіше, оскільки можна протестувати логіку обчислень, взаємодії з API та визначення порушень швидкості окремо.

## 10. Зменшення зв'язності та покращення когезії
**Покращено:**

Тепер компоненти взаємодіють один з одним через чітко визначені інтерфейси, знижуючи зв'язність між частинами програми. Кожен модуль виконує свою чітко визначену задачу: модулі для обчислення швидкості, для взаємодії з API, для аналізу порушень і т.д., що зберігає високий рівень когезії та дозволяє швидко міняти окремі компоненти без впливу на інші частини програми.

## 11. Принцип найменшого здивування (Law of Demeter)
**Покращено:**

Принцип "не звертатися до методів об'єктів, які не є частинами безпосереднього оточення" був дотриманий завдяки розбиттю функціональності на окремі методи та використанню чітко визначених інтерфейсів. Наприклад, функція `find_violations_places` працює з координатами, не залучаючи надмірну кількість залежностей.

## 12. YAGNI (You Aren't Gonna Need It)
**Покращено:**

Замість додавання зайвих складних абстракцій, кожна зміна була спрямована на оптимізацію коду та полегшення тестування, без додавання непотрібних функцій або абстракцій. Програма залишається гнучкою та не перевантаженою зайвими компонентами.

** **
** **


# Опис Моделі Архітектури

Для покращення організації коду та підвищення його масштабованості, тестованості й підтримуваності були внесені кілька важливих змін в архітектуру  проєкту на основі принципів об'єктно-орієнтованого програмування (ООП) і архітектурних патернів.

## 1. Моделі та їх опис

### **BusDataHandler** (Обробка даних автобусів)

**Зміни:** Створено єдиний клас для обробки даних автобусів. Цей клас відповідає за завантаження даних автобусів з файлів, попередню їх обробку та збереження результатів.

**Обов'язки:**
- Завантаження даних автобусів із файлів.
- Збереження результатів обробки даних.
- Перевірка коректності даних.
- Використовує методи з `api_utils` для з'єднання з API.

### **SpeedViolationChecker** (Перевірка порушень швидкості)

**Зміни:** Клас перевірки порушень швидкості став більш гнучким завдяки впровадженню патерну "Стратегія". Тепер для перевірки швидкості використовуються різні стратегії (наприклад, HaversineSpeedCalculationStrategy).

**Обов'язки:**
- Використовує стратегію для обчислення швидкості.
- Порівнює обчислену швидкість з максимально дозволеною.
- Генерує список порушень швидкості.
- Зберігає координати порушень.

### **SpeedViolationCheckerFactory** (Фабрика порушень швидкості)

**Зміни:** Використання патерну "Фабрика" для створення об'єктів `SpeedViolationChecker`, що дозволяє на основі певних параметрів вибирати стратегії обчислення швидкості.

**Обов'язки:**
- Створює екземпляри `SpeedViolationChecker` за допомогою фабричного методу, передаючи стратегії для обчислення швидкості.

### **SpeedCalculationFactory** (Фабрика обчислення швидкості)

**Зміни:** Впроваджено патерн "Фабрика", який дозволяє створювати різні стратегії обчислення швидкості без зміни основного коду програми.

**Обов'язки:**
- Створює об'єкти для обчислення швидкості, які реалізують різні алгоритми (наприклад, HaversineSpeedCalculationStrategy).
- Це дозволяє обирати алгоритм обчислення швидкості залежно від контексту (наприклад, для різних форматів даних).

### **PunctualityAnalyzer** (Аналіз пунктуальності)

**Зміни:** Окремий клас для аналізу пунктуальності автобусів. Використовує завантажені дані і перевіряє відповідність розкладу.

**Обов'язки:**
- Аналізує дані про пунктуальність автобусів.
- Визначає, які автобуси не відповідають вимогам розкладу.

### **ViolationClusterer** (Кластеризація порушень швидкості)

**Зміни:** Окремий клас для кластеризації порушень швидкості на основі географічної близькості (з використанням `find_violations_places`).

**Обов'язки:**
- Кластеризує місця порушень швидкості за певним порогом відстані.
- Допомагає виявляти місця, де порушення відбуваються часто, що може вказувати на проблеми з інфраструктурою.

### **APIUtils** (Утиліти для роботи з API)

**Зміни:** Зроблено окремі утилітні функції для роботи з API. Це дозволяє спростити з'єднання з різними сервісами і зменшити залежність основних класів від деталей реалізації API.

**Обов'язки:**
- Взаємодіє з API для отримання необхідних даних (наприклад, зупинки автобусів, час прибуття, точність).

### **GeoUtils** (Географічні утиліти)

**Зміни:** Створено окремий модуль для обчислення географічних відстаней. Це дозволяє централізувати географічні обчислення (наприклад, для перевірки швидкості або кластеризації порушень).

**Обов'язки:**
- Обчислення відстані між точками за допомогою формули Haversine.

### **Main** (Основний модуль)

**Зміни:** Основний файл для запуску аналізу даних. Раніше в основному файлі знаходилась вся логіка, тепер це лише точка входу, що викликає відповідні методи для обробки даних.

**Обов'язки:**
- Завантаження даних.
- Виклик функцій для аналізу швидкості, порушень, пунктуальності.
- Виведення результатів аналізу.

## 2. Зміни, що були внесені в архітектуру:

### **Патерн "Стратегія" (Strategy Pattern):**
- Використано для обчислення швидкості. Клас `SpeedCalculationStrategy` є абстракцією для різних стратегій обчислення швидкості (наприклад, `HaversineSpeedCalculationStrategy`). Це дозволяє змінювати стратегії без модифікації основного коду програми.

### **Патерн "Фабрика" (Factory Pattern):**
- Для створення об'єктів `SpeedViolationChecker` і стратегій швидкості використовується фабрика. Це забезпечує гнучкість у створенні об'єктів без необхідності змінювати код програми.

### **Розподіл відповідальностей (Single Responsibility Principle):**
- Кожен клас виконує тільки одну задачу: обчислення швидкості, перевірка порушень, аналіз пунктуальності, кластеризація порушень, робота з API тощо. Це полегшує підтримку та тестування.

### **Принцип відкритості/закритості (Open/Closed Principle):**
- Система тепер дозволяє додавати нові стратегії без змін в основному коді. Наприклад, можна додавати нові алгоритми для обчислення швидкості або нові типи порушень.

### **Інкапсуляція (Encapsulation):**
- Деталі реалізації (наприклад, обчислення швидкості або кластеризація порушень) приховані в окремих класах. Взаємодія між компонентами здійснюється через чітко визначені інтерфейси.

### **Тестування:**
- Завдяки розподілу на менші функції та модулі, кожну частину програми тепер можна тестувати окремо. Це дозволяє ефективніше писати юніт-тести для кожної окремої частини.

### **Зниження зв'язності (Loose Coupling):**
- Компоненти взаємодіють один з одним через чітко визначені інтерфейси (наприклад, `SpeedViolationChecker` використовує стратегії обчислення швидкості через абстракції, а не через конкретні реалізації). Це забезпечує гнучкість у зміні реалізацій без впливу на інші частини програми.

### **Масштабованість:**
- Структура коду дозволяє без проблем додавати нові стратегії, перевірки або функціональність (наприклад, нові алгоритми для обчислення швидкості або нові перевірки для пунктуальності), не змінюючи основний код програми.
