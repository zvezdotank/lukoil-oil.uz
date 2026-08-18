# Фотографии сайта: арт-дирекция и промпты

## Почему сейчас выглядит слабо

Текущие кадры собраны из трёх источников: мелкие пережатые снимки с lukoil.ru
(220–1400 px, часть уже с артефактами), AI-сток с transoil-group.com (узнаваемый
«глянец»: неестественные блики, вылизанные поверхности) и любительские снимки
с Wikimedia. У них разная оптика, свет, зерно и дистанция. Фильтр `grayscale`
скрывает разнобой по цвету, но не по фактуре — глаз всё равно читает «набор
случайных картинок», а не съёмку.

## Пять правил, которые делают фото профессиональными

**1. Одна серия, а не коллекция.** Все кадры должны выглядеть снятыми одним
фотографом за один день: одна оптика, один тип света, одна цветовая температура,
одинаковое зерно. Поэтому у всех промптов ниже общий стилевой префикс — его
менять нельзя, меняется только сюжетная часть.

**2. Обработка как часть айдентики.** Сейчас `filter: grayscale(1) contrast(1.08)`.
Сильнее работает **дуотон**: тени — угольный `#201e1d`, света — фирменный красный
`#ec3013`. Фото перестают быть иллюстрациями и становятся частью фирменного стиля,
а разнородность источников исчезает полностью. Вариант включается одной правкой
в `site.css` — скажите, и переключу.

**3. Кадр под слот, а не кроп по факту.** Слоты на сайте имеют жёсткие пропорции.
Генерировать нужно сразу в нужной, с запасом воздуха по краям, иначе при кропе
режется композиция. Пропорции указаны в таблице.

**4. Кадр доказывает тезис.** Не «красивое масло льётся в свете софтбокса» — это
стоковый штамп, который читается как «нам нечего показать». Вместо этого:
паллета с бочками под погрузчиком, инженер с картой смазки у редуктора,
счётчик на отгрузке. Фото должно подтверждать то, что написано рядом.

**5. Что не генерировать.** Нельзя делать вымышленные бочки и канистры
с логотипом ЛУКОЙЛ — это подделка фирменной продукции. Снимки продукции
(восемь канистр 800×800) и бочек на складе — подлинные, с сайта производителя,
их оставляем. Генерируем только нейтральные производственные сцены без
брендинга: логотип на сайте живёт в шапке, фавиконе и красном акценте.

---

## Общий стилевой префикс

Ставится в начало **каждого** промпта без изменений:

```
Documentary industrial photography, single consistent series. Shot on 40mm lens,
f/4, natural available light with one soft directional source from camera left,
neutral daylight white balance around 5200K. Muted desaturated palette: graphite,
steel grey, concrete, with one deliberate accent of industrial red. Fine 35mm
film grain, slight vignette, no HDR, no glossy CGI look, no lens flare.
Deep focus, everything readable. No people looking at camera, no visible brand
logos, no text, no watermarks.
```

## Общий негативный промпт

```
glossy stock photo, plastic CGI render, oversaturated colors, teal and orange
grading, dramatic god rays, fake bokeh, floating oil droplets, generic 3d
mechanical parts, watermark, text overlay, brand logos, distorted machinery,
extra limbs
```

---

## Слоты и сюжеты

Пропорции Gemini: `9:16`, `4:3`, `16:9`, `1:1`.

| Файл | Где на сайте | Пропорция | Сюжет |
|---|---|---|---|
| `hero-drums` | герой главной, вертикальная полоса слева | **9:16** | стеллаж с бочками |
| `ind-gears` | плитка «Индустриальные и редукторные» | 16:9 | вскрытый редуктор |
| `ind-cnc` | плитка «Гидравлические» | 16:9 | гидроцилиндры пресса |
| `ind-compressor` | плитка «Компрессорные и турбинные» | 16:9 | винтовой компрессор |
| `ind-boiler` | плитка «СОЖ и теплоносители» | 16:9 | термомасляный узел |
| `ind-transmission` | плитка «Моторные и трансмиссионные» | 16:9 | двигатель тягача в цеху |
| `ind-bearing` | плитка «Смазки и техжидкости» | 16:9 | подшипник и шприц-нагнетатель |
| `fleet` | отрасль «Автопарки и логистика» | **4:3** | колонна тягачей |
| `ind-pumps` | отрасль «Промышленность и заводы» | **4:3** | пролёт цеха |
| `agro` | отрасль «Сельхозтехника» | **4:3** | трактор в поле |
| `bottling` | «Склад, отгрузка, документы» на главной | 16:9 | погрузчик с паллетой |
| `plant` | «Документы на партию», страница «О компании» | 16:9 | приёмка партии |
| `map` | блок под контактами | 16:9 | ворота склада, отгрузка |
| `ind-turbine` | кадр применения, компрессорные/гидравлика | 16:9 | турбинный ротор |
| `ind-power` | кадр применения, индустриальные | 16:9 | подстанция предприятия |
| `ind-grease` | кадр применения, смазки | 16:9 | закладка смазки в узел |
| `ind-engine` | кадр применения, смазки | 16:9 | дизель на стенде |
| `car` | кадр применения, моторные | 16:9 | подъёмник в сервисе |

---

## Промпты

Сюжетная часть — дописывается **после** общего префикса.

### hero-drums · 9:16 — главный кадр сайта

```
Vertical composition. Warehouse aisle with steel drums stacked two high on wooden
pallets in racking, receding into depth. Concrete floor with painted yellow lane
markings. Cool daylight falling from high side windows. Drums unbranded, plain
dark steel with one red drum in the middle ground as the only accent. Camera at
chest height, aisle centered, generous headroom above the racking.
```

### ind-gears · 16:9 — индустриальные и редукторные

```
Open industrial gearbox on a factory floor, inspection cover removed, helical
gear teeth wet with fresh oil, oil film catching the light. Shot slightly from
above at working distance. Steel and graphite tones, red painted housing edge as
accent. Workshop background softly out of focus.
```

### ind-cnc · 16:9 — гидравлические

```
Hydraulic press in a machine shop, three chromed cylinder rods extended, hoses
and manifold block visible, pressure gauge in frame. Side light raking across
the polished rods. Red control lever as the single colour accent.
```

### ind-compressor · 16:9 — компрессорные и турбинные

```
Screw compressor unit in a plant compressor room, panel opened showing the oil
separator tank and cooling lines, pressure gauges and valves. Cool overhead
light, painted concrete floor, red isolation valve handle as accent.
```

### ind-boiler · 16:9 — СОЖ и теплоносители

```
Thermal oil heating unit in a production hall: insulated piping, expansion
vessel, circulation pump and temperature gauges on a steel frame. Warm metal and
insulation tones against grey concrete, red pipe marking bands as accent.
```

### ind-transmission · 16:9 — моторные и трансмиссионные

```
Heavy truck diesel engine on a workshop stand, valve cover off, camshaft and
rockers visible, oil sheen on machined surfaces. Tools laid out on a steel bench
in the foreground. Workshop lighting, red tool chest edge as accent.
```

### ind-bearing · 16:9 — смазки и техжидкости

```
Large rolling bearing on a shaft, half-open housing, technician's gloved hand
applying grease with a lever grease gun. Amber grease clearly visible in the
raceway. Close working distance, shallow depth on the background only.
```

### fleet · 4:3 — автопарки и логистика

```
Row of long-haul tractor units parked diagonally on a transport company yard at
early morning, side three-quarter view, cabs unbranded plain white and grey.
Wet asphalt reflecting cool sky, fuel and service area in the background. One
red cab in the line as accent.
```

### ind-pumps · 4:3 — промышленность и заводы

```
Wide interior of a production hall: two rows of process pumps and motors on
concrete plinths, overhead pipework and cable trays, crane rail near the ceiling.
Daylight from clerestory windows. Grey and steel palette, red fire line as accent.
```

### agro · 4:3 — сельхозтехника

```
Tractor with a mounted sprayer working a cultivated field in flat late-afternoon
light, three-quarter front view, dust rising from the wheels. Wide agricultural
plain in the background, low horizon, generous sky. Tractor body plain dark
green, no brand marks.
```

### bottling · 16:9 — склад, отгрузка, документы

```
Forklift lifting a pallet of steel drums inside a distribution warehouse,
operator in the cab in profile, racking and stacked pallets behind. Open loading
door on the right spilling daylight across the concrete floor. Yellow forklift as
the warm accent against cool grey.
```

### plant · 16:9 — документы на партию

```
Goods-in area of a lubricants warehouse: pallets of steel drums under shrink
wrap, a steel desk with a clipboard, batch documents and a barcode scanner in
the foreground, warehouse depth behind. Even daylight, no people in frame.
```

### map · 16:9 — блок у контактов

```
Exterior of an industrial warehouse: loading dock with two open sectional doors,
a truck backed up to the ramp, concrete apron and yard markings, low perimeter
fence. Flat overcast light, early morning, no signage on the building.
```

### ind-turbine · 16:9

```
Steam turbine rotor with rows of blades resting on maintenance supports in a
power plant workshop, protective mats on the floor, overhead crane hook above.
Cool grey palette, red crane hook as accent.
```

### ind-power · 16:9

```
Outdoor electrical substation of an industrial plant: transformers, insulators
and busbars in receding rows, gravel ground, chain-link fence in the near
foreground. Overcast flat light, grey and steel tones.
```

### ind-grease · 16:9

```
Central lubrication system on a production line: metering block, distribution
lines and grease nipples on a machine frame, fresh grease at a fitting.
Close working distance, machine surfaces worn from real use.
```

### ind-engine · 16:9

```
Industrial diesel generator set in an engine room: engine block, exhaust
manifold with heat wrapping, control cabinet beside it, painted floor with
containment kerb. Even artificial light, red emergency stop button as accent.
```

### car · 16:9

```
Passenger car on a two-post lift in a service bay, viewed from below and to the
side, oil drain pan positioned under the sump, tool trolley beside the lift.
Clean workshop, cool fluorescent light, car unbranded mid-size sedan.
```

---

## Что делать с готовыми файлами

Складывайте в `img/src/` под теми же именами (`hero-drums.jpg`, `ind-gears.jpg`
и так далее) — я прогоню их через пайплайн:

1. ресайз под слот (герой 1200 px по ширине, сцены 1120, плитки 560);
2. кроп в точную пропорцию слота по центру;
3. `webp` + `jpg`-фолбэк, качество 78/72, прогрессивный;
4. генерация `-t` миниатюр для плиток;
5. обновление `width`/`height` в разметке и версии кэша.

Один кадр в 16:9 после обработки весит 40–80 КБ, вертикальный герой — около 55 КБ.
Бюджет главной сохранится в пределах 250–300 КБ.
