# CyberSafe — Получение доступа к прошивке современной компьютерной платы с использованием различных техник ревер-инжиниринга

**Исследование четырёх потенциальных векторов доступа к устройству CyberSafe на базе RP2040.**

> **Краткий итог:** рассмотрено 4 потенциальных вектора доступа; 2 подтверждены на физическом устройстве.

## Результаты

| Вектор | Статус | Результат |
|---|---|---|
| Штатный загрузочный механизм BOOTSEL | **Подтверждён на устройстве** | Получен полный дамп Flash объёмом 2 МиБ; попытка загрузить модифицированную прошивку с отключённой проверкой пароля не удалась. |
| Автоматизированный перебор PIN | **Подтверждён на устройстве** | Raspberry Pi имитирует ввод энкодером, камера контролирует интерфейс; перебор занял около 8 часов и записан на видео. |
| Прямое чтение внешней Flash-памяти | **Гипотеза** | Не проверялось; требуется дополнительное оборудование. |
| Подключение по SWD | **Гипотеза** | Не проверялось; физическое подключение может повредить устройство. |

**Итог исследования: 4 вектора рассмотрены, 2 подтверждены на практике.**

## Структура репозитория

```text
.
├── README.md
├── report.md
├── vector_1/
│   ├── README.md        # Краткое описание вектора 1
│   └── report.md        # Подробный отчёт по BOOTSEL
├── vector_2/
│   ├── README.md        # Краткое описание вектора 2
│   └── report.md        # Подробный отчёт по перебору PIN
├── vector_3/
│   ├── README.md        # Краткое описание вектора 3
│   └── report.md        # Подробный отчёт по гипотезе Flash
├── vector_4/
│   ├── README.md        # Краткое описание вектора 4
│   └── report.md        # Подробный отчёт по гипотезе SWD
└── evidence/
    ├── README.md
    ├── artifacts/
    │   ├── dump.bin
    │   └── dump_strings.txt
    ├── boot_files/
    │   ├── INDEX.HTM
    │   └── INFO_UF2.TXT
    ├── files_from_cybersafe/
    │   └── your_prize.zip
    ├── photos/
    │   ├── device_01.jpg
    │   ├── device_02.jpg
    │   ├── raspberrypi.jpg
    │   └── rp2040_pins.png
    └── scripts/
        ├── led_check.py
        └── main.py
```

## Статусы и ограничения

- **Подтверждено на устройстве** — эксперимент проведён на физическом устройстве и результат зафиксирован.
- **Гипотеза** — эксперимент не проводился.

Видеозапись перебора PIN размещена на Google Drive и доступна из [подробного отчёта по вектору 2](vector_2/report.md#5-видеодоказательство). Прямое чтение Flash внешним программатором и подключение по SWD не проводились.

---

# CyberSafe — Accessing Firmware on a Modern Computer Board Through Reverse Engineering

**An assessment of four potential access vectors for the RP2040-based CyberSafe device.**

> **Summary:** 4 potential access vectors were assessed; 2 were confirmed on the physical device.

## Results

| Vector | Status | Result |
|---|---|---|
| Standard BOOTSEL boot mechanism | **Confirmed on-device** | A full 2 MiB Flash dump was acquired; an attempt to load modified firmware with password verification disabled was unsuccessful. |
| Automated PIN brute force | **Confirmed on-device** | A Raspberry Pi simulated encoder input while a camera monitored the interface; the attempt took about 8 hours and was recorded on video. |
| Direct readout of external Flash | **Hypothesis** | Not tested; additional equipment is required. |
| SWD connection | **Hypothesis** | Not tested; physical probing may damage the device. |

**Assessment outcome: 4 vectors considered, 2 confirmed in practice.**

## Repository layout

```text
.
├── README.md
├── report.md
├── vector_1/
│   ├── README.md        # Vector 1 summary
│   └── report.md        # Detailed BOOTSEL report
├── vector_2/
│   ├── README.md        # Vector 2 summary
│   └── report.md        # Detailed PIN brute-force report
├── vector_3/
│   ├── README.md        # Vector 3 summary
│   └── report.md        # Detailed Flash hypothesis report
├── vector_4/
│   ├── README.md        # Vector 4 summary
│   └── report.md        # Detailed SWD hypothesis report
└── evidence/
    ├── README.md
    ├── artifacts/
    │   ├── dump.bin
    │   └── dump_strings.txt
    ├── boot_files/
    │   ├── INDEX.HTM
    │   └── INFO_UF2.TXT
    ├── files_from_cybersafe/
    │   └── your_prize.zip
    ├── photos/
    │   ├── device_01.jpg
    │   ├── device_02.jpg
    │   ├── raspberrypi.jpg
    │   └── rp2040_pins.png
    └── scripts/
        ├── led_check.py
        └── main.py
```

## Status and limitations

- **Confirmed on-device** — the test was performed on the physical device and the result was recorded.
- **Hypothesis** — the test was not performed.

The PIN brute-force video is hosted on Google Drive and linked from the [detailed Vector 2 report](vector_2/report.md#5-видеодоказательство). Direct readout of the external Flash with a programmer and SWD access were not performed.