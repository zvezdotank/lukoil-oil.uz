# Фотографии сайта: арт-дирекция и промпты

## Позиционирование

ЛУКОЙЛ — масло для **нового оборудования**, а не для доживающего свой век парка.
Поэтому в кадре: недавно введённая в эксплуатацию техника, заводская окраска без
сколов, аккуратная разводка кабелей, эпоксидные полы, светодиодный свет, цифровые
контроллеры вместо стрелочных манометров с треснувшим стеклом. Ни ржавчины, ни
подтёков, ни советского цеха.

Это меняет смысл: не «мы работаем с тем, что осталось», а «нас берут туда, где
оборудование стоит дорого и простой недопустим».

## Обработка: дуотон

На сайте включён дуотон — тени уходят в графит `#201e1d`, средние тона в фирменный
красный `#ec3013`, света в цвет фона `#f3f2f2`. Реализован SVG-фильтром `#duo`
(см. `build.py`), применяется классом `.grayscale`.

Из этого следует требование к кадрам: **важен тональный контраст, а не цвет**.
Дуотон уничтожает цветовые различия, остаются форма, свет и геометрия. Кадр, где
объект отличается от фона только цветом, после конвертации превратится в кашу.
Поэтому в промптах требуется чёткое разделение переднего плана, объекта и фона по
светлоте.

## Правила

**1. Одна серия.** Все кадры сняты как будто одним фотографом за один день: одна
оптика, один свет, одна цветовая температура. Общий префикс ниже не меняется.

**2. Никакого плёночного зерна и виньетки.** Это приёмы «состаривания», они прямо
противоречат задаче. Нужна чистая цифровая съёмка.

**3. Кадр под слот.** Пропорции жёсткие: герой — 9:16, отрасли — 4:3, остальное —
16:9. Генерировать сразу в нужной, с запасом по краям.

**4. Кадр доказывает тезис.** Не «масло льётся в свете софтбокса», а конкретная
машина, которую этим маслом обслуживают.

**5. Без брендинга.** Не генерировать бочки и канистры с логотипом ЛУКОЙЛ — это
подделка фирменной продукции. Снимки продукции подлинные, с сайта производителя.
Фирменность держат шапка, фавикон и красный акцент.

---

## Общий стилевой префикс

Ставится в начало **каждого** промпта без изменений:

```
Clean modern industrial photography, single consistent series. Recently
commissioned equipment in a bright, well-maintained facility: factory-fresh
paint, unscratched panels, tidy cable routing, epoxy-coated floors, LED lighting,
digital control panels. Shot on 35mm lens, f/5.6, even soft daylight from large
windows combined with neutral overhead LED, white balance 5600K. Crisp digital
capture, no film grain, no vignette, no HDR halos. Strong graphic composition
with clear tonal separation between foreground, subject and background — the
image must stay readable when converted to a two-tone duotone. No people looking
at camera, no brand logos, no text, no watermarks.
```

## Общий негативный промпт

```
rust, corrosion, peeling paint, chipped enamel, grime, oil stains on the floor,
soviet-era factory, abandoned plant, dim cluttered warehouse, vintage machinery,
cracked analog gauges, film grain, sepia, vintage look, glossy CGI render,
oversaturated colors, teal and orange grading, dramatic god rays, fake bokeh,
floating oil droplets, watermark, text overlay, brand logos
```

---

## Слоты

| Файл | Где на сайте | Пропорция |
|---|---|---|
| `hero-drums` | герой главной, вертикальная полоса | **9:16** |
| `ind-gears` | плитка «Индустриальные и редукторные» | 16:9 |
| `ind-cnc` | плитка «Гидравлические» | 16:9 |
| `ind-compressor` | плитка «Компрессорные и турбинные» | 16:9 |
| `ind-boiler` | плитка «СОЖ и теплоносители» | 16:9 |
| `ind-transmission` | плитка «Моторные и трансмиссионные» | 16:9 |
| `ind-bearing` | плитка «Смазки и техжидкости» | 16:9 |
| `fleet` | отрасль «Автопарки и логистика» | **4:3** |
| `ind-pumps` | отрасль «Промышленность и заводы» | **4:3** |
| `agro` | отрасль «Сельхозтехника» | **4:3** |
| `bottling` | «Склад, отгрузка, документы» | 16:9 |
| `plant` | «Документы на партию» | 16:9 |
| `map` | блок у контактов | 16:9 |
| `ind-turbine` | кадр применения | 16:9 |
| `ind-power` | кадр применения | 16:9 |
| `ind-grease` | кадр применения | 16:9 |
| `ind-engine` | кадр применения | 16:9 |
| `car` | кадр применения | 16:9 |

---

## Промпты

Сюжетная часть дописывается **после** общего префикса.

### hero-drums · 9:16 — главный кадр сайта

```
Vertical composition. Aisle of a newly built distribution warehouse: tall powder
coated steel racking, new unmarked steel drums on clean pallets stacked two high,
receding into depth. Bright epoxy floor with fresh lane markings, linear LED
fixtures running along the ceiling. Camera at chest height, aisle centered,
generous headroom above the racking. Cool bright interior, dark drums reading
clearly against the light floor.
```

### ind-gears · 16:9 — индустриальные и редукторные

```
Modern planetary gearbox on a production line, inspection cover lifted, helical
gear teeth glossy with clean fresh oil. New painted housing, machined flanges,
digital condition-monitoring sensor mounted on the casing with a tidy cable.
Bright machine hall behind, softly defocused.
```

### ind-cnc · 16:9 — гидравлические

```
Modern hydraulic press with CNC control, three chromed cylinder rods extended,
new hydraulic manifold block, braided hoses in clean routing clips, digital
pressure display on the panel. Raking side light along the polished rods, light
machine shop behind.
```

### ind-compressor · 16:9 — компрессорные и турбинные

```
Modern screw compressor in a clean compressor room, sound-insulated enclosure
open on one side showing the oil separator tank, new cooling lines and a digital
touchscreen controller. Bright white walls, epoxy floor, stainless pipework.
```

### ind-boiler · 16:9 — СОЖ и теплоносители

```
Modern thermal oil heating skid: stainless steel pipework, expansion vessel,
circulation pump and digital temperature transmitters mounted on a new painted
frame. Clean production hall, bright even light, no insulation damage.
```

### ind-transmission · 16:9 — моторные и трансмиссионные

```
Modern Euro 6 truck diesel engine mounted on a workshop test stand, valve cover
removed, camshaft and rockers with a clean oil film, new wiring harness routed
along the block. Bright service bay, tools laid out on a stainless bench.
```

### ind-bearing · 16:9 — смазки и техжидкости

```
Large new rolling bearing in a split housing on a machine shaft, automatic
single-point lubricator screwed into the fitting, fresh grease visible in the
raceway. Machined surfaces clean and bright, modern machine frame behind.
```

### fleet · 4:3 — автопарки и логистика

```
Row of new aerodynamic long-haul tractor units parked diagonally on a freshly
paved transport yard at early morning, side three-quarter view, LED headlights
lit, plain white and graphite cabs with no markings. Modern service building and
fuel island behind, clean asphalt with crisp lane paint.
```

### ind-pumps · 4:3 — промышленность и заводы

```
Wide interior of a modern production hall: two rows of new process pumps and
motors on painted plinths, stainless pipework and tidy cable trays overhead,
overhead crane rail near the ceiling. Bright daylight from clerestory windows,
white walls, epoxy floor with marked walkways.
```

### agro · 4:3 — сельхозтехника

```
New high-horsepower tractor with a mounted sprayer working a cultivated field in
flat late-afternoon light, three-quarter front view, GPS antenna on the cab roof,
clean bodywork with no markings. Wide agricultural plain, low horizon, generous
sky, crisp furrow lines leading into the frame.
```

### bottling · 16:9 — склад, отгрузка, документы

```
Electric forklift lifting a pallet of new steel drums inside a modern
distribution warehouse, operator in the cab in profile, tall racking behind.
Open dock door on the right spilling daylight across the epoxy floor. Clean
bright interior, strong tonal separation between the dark pallet and the pale
floor.
```

### plant · 16:9 — документы на партию

```
Goods-in area of a modern lubricants warehouse: shrink-wrapped pallets of new
steel drums under bright LED light, a stainless desk with a tablet and a barcode
scanner in the foreground, racking receding behind. No people in frame, clean
floor, crisp geometry.
```

### map · 16:9 — блок у контактов

```
Exterior of a modern logistics warehouse: three loading docks with dock shelters
and levellers, a new box truck backed up to one of them, clean concrete apron
with fresh markings, low landscaped verge. Flat bright overcast light, no signage
on the building.
```

### ind-turbine · 16:9

```
Modern steam turbine rotor with polished blade rows resting on maintenance
supports in a bright, clean turbine hall, protective mats under it, overhead
crane hook above. Stainless and light grey surfaces, strong graphic repetition
of the blades.
```

### ind-power · 16:9

```
Modern indoor switchgear room of an industrial plant: a row of new metal-clad
switchgear cubicles with digital protection relays, clean cable trench covers,
bright even lighting, white walls.
```

### ind-grease · 16:9

```
Modern centralised lubrication system on a production line: progressive metering
block, stainless distribution lines in tidy clips, digital pump unit with a
level indicator mounted on a new machine frame. Clean surfaces, bright light.
```

### ind-engine · 16:9

```
Modern containerised diesel generator set in a clean plant engine room: new
engine block, insulated exhaust manifold, digital control cabinet beside it,
epoxy floor with a marked containment kerb. Even bright artificial light.
```

### car · 16:9

```
Modern car service bay: a recent mid-size sedan raised on a two-post lift, oil
drain unit positioned under the sump, stainless tool trolley beside it. Bright
white workshop with epoxy floor and LED panels, no branding anywhere.
```

---

## Что делать с готовыми файлами

Складывайте в `img/src/` под теми же именами (`hero-drums.jpg`, `ind-gears.jpg`),
дальше пайплайн:

1. кроп в точную пропорцию слота по центру;
2. ресайз (герой 1200 px по ширине, сцены 1120, плитки 560);
3. `webp` + `jpg`-фолбэк, качество 78/72, прогрессивный;
4. генерация `-t` миниатюр;
5. обновление `width`/`height` в разметке и версии кэша `V` в `build.py`.

Кадр 16:9 после обработки — 40–80 КБ, вертикальный герой — около 55 КБ.
Бюджет главной остаётся в пределах 250–300 КБ.
