# Patent Diagram Creating RAG Knowledge Base
## Generate Patent-Quality Diagrams for Software/AI Inventions

---

## Purpose

This skill creates patent-quality diagrams including system architecture diagrams, flowcharts, data flow diagrams, and UI mockups that meet USPTO requirements and enhance patent application quality.

---

## Required Diagram Types

### 1. System/Network Diagram (FIG. 1)

**Purpose:** Show all major components and their connections

**Elements to Include:**
- User devices (mobile, desktop, IoT)
- Servers (application, database, ML inference)
- Network connections (internet, LAN, API)
- External services (third-party APIs, cloud services)
- Data stores (databases, caches, file systems)

**Example Structure:**
```
+------------------+     +-----------------+     +------------------+
|   User Device    |---->|   API Gateway   |---->|  Application     |
|  (Mobile/Web)    |     |                 |     |    Server        |
+------------------+     +-----------------+     +------------------+
                                                        |
                                                        v
                              +------------------+     +------------------+
                              |   ML Inference   |<----|    Database      |
                              |     Service      |     |                  |
                              +------------------+     +------------------+
```

**ASCII Diagram Template:**
```
┌─────────────────────────────────────────────────────────────────┐
│                         SYSTEM 100                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐        ┌──────────┐        ┌──────────┐          │
│  │ Client   │───────>│  Server  │───────>│ Database │          │
│  │ Device   │  102   │   104    │  106   │   108    │          │
│  │   101    │<───────│          │<───────│          │          │
│  └──────────┘        └──────────┘        └──────────┘          │
│       │                   │                   │                 │
│       │              ┌────┴────┐              │                 │
│       │              │   ML    │              │                 │
│       └─────────────>│ Engine  │<─────────────┘                 │
│                      │   110   │                                │
│                      └─────────┘                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Hardware Block Diagram (FIG. 2)

**Purpose:** Show processor, memory, I/O relationships

**Required Components:**
- Processor (CPU/GPU/TPU)
- Memory (RAM, Cache)
- Storage (SSD, HDD)
- I/O interfaces
- Bus connections

**Template:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPUTING DEVICE 200                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                    PROCESSOR 202                        │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │    │
│  │  │  Core 1  │  │  Core 2  │  │  Core N  │             │    │
│  │  │   204    │  │   206    │  │   208    │             │    │
│  │  └──────────┘  └──────────┘  └──────────┘             │    │
│  └────────────────────────────────────────────────────────┘    │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          │                                      │
│                    ┌─────┴─────┐                                │
│                    │ SYSTEM BUS│                                │
│                    │    210    │                                │
│                    └─────┬─────┘                                │
│         ┌────────────────┼────────────────┐                     │
│         │                │                │                     │
│  ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐             │
│  │   MEMORY    │  │   STORAGE   │  │   NETWORK   │             │
│  │     212     │  │     214     │  │  INTERFACE  │             │
│  │             │  │             │  │     216     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Method Flowchart (FIG. 3, 4, 5...)

**Purpose:** Show step-by-step software process

**Required Elements:**
- Start/End (rounded rectangles or ovals)
- Process steps (rectangles)
- Decisions (diamonds)
- Data flow arrows
- Reference numbers (301, 302, etc.)

**Template:**
```
                    ┌─────────────────┐
                    │     START       │
                    │      300        │
                    └────────┬────────┘
                             │
                             v
                    ┌─────────────────┐
                    │  Receive Input  │
                    │      302        │
                    └────────┬────────┘
                             │
                             v
                    ┌─────────────────┐
                    │ Preprocess Data │
                    │      304        │
                    └────────┬────────┘
                             │
                             v
                       ◇───────────◇
                      ╱             ╲
                     ╱   Valid       ╲
                    ╱    Input?       ╲
                   ╱       306        ╲
                  ◇─────────────────────◇
                  │YES               NO│
                  v                    v
         ┌─────────────────┐  ┌─────────────────┐
         │  Apply ML Model │  │  Return Error   │
         │      308        │  │      310        │
         └────────┬────────┘  └────────┬────────┘
                  │                    │
                  v                    │
         ┌─────────────────┐          │
         │ Generate Output │          │
         │      312        │          │
         └────────┬────────┘          │
                  │                    │
                  └──────────┬─────────┘
                             │
                             v
                    ┌─────────────────┐
                    │      END        │
                    │      314        │
                    └─────────────────┘
```

### 4. Data Flow Diagram (FIG. 6)

**Purpose:** Show how data moves through the system

**Template:**
```
┌─────────────────────────────────────────────────────────────────┐
│                      DATA FLOW 600                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Input    Preprocessed     Feature        Prediction      │
│     Data         Data          Vectors          Output         │
│      │            │              │               │              │
│      v            v              v               v              │
│  ┌──────┐    ┌──────┐       ┌──────┐        ┌──────┐           │
│  │ Raw  │───>│Clean │──────>│Extract│───────>│ ML   │──>Result │
│  │ Data │602 │ Data │ 604   │Features│ 606  │Model │ 608      │
│  │      │    │      │       │       │       │      │           │
│  └──────┘    └──────┘       └──────┘        └──────┘           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5. UI Mockup (FIG. 7)

**Purpose:** Show user interface for software inventions

**Template:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE 700                           │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │                    Header/Navigation 702                    │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌───────────────────────┐  ┌─────────────────────────────────┐ │
│ │   Input Panel 704     │  │      Results Panel 706          │ │
│ │ ┌───────────────────┐ │  │ ┌─────────────────────────────┐ │ │
│ │ │ Text Field 708    │ │  │ │    Output Display 712       │ │ │
│ │ └───────────────────┘ │  │ │                             │ │ │
│ │                       │  │ │    [Prediction: 95%]        │ │ │
│ │ ┌───────────────────┐ │  │ │                             │ │ │
│ │ │ Submit Button 710 │ │  │ └─────────────────────────────┘ │ │
│ │ └───────────────────┘ │  │                                 │ │
│ └───────────────────────┘  └─────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6. Swimlane Diagram (FIG. 8)

**Purpose:** Show interactions between multiple entities

**Template:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    SWIMLANE DIAGRAM 800                         │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│    CLIENT    │    SERVER    │   ML ENGINE  │    DATABASE       │
├──────────────┼──────────────┼──────────────┼───────────────────┤
│      │       │      │       │      │       │       │           │
│  ┌───┴───┐   │      │       │      │       │       │           │
│  │Request│───┼──────>       │      │       │       │           │
│  │  802  │   │   ┌──┴──┐    │      │       │       │           │
│  └───────┘   │   │Parse│    │      │       │       │           │
│      │       │   │ 804 │────┼──────>       │       │           │
│      │       │   └─────┘    │   ┌──┴──┐    │       │           │
│      │       │      │       │   │Infer│────┼───────>           │
│      │       │      │       │   │ 806 │    │    ┌──┴──┐        │
│      │       │      │       │   └─────┘    │    │Query│        │
│      │       │      │       │      │<──────┼────│ 808 │        │
│      │       │      │       │      │       │    └─────┘        │
│      │       │      │<──────┼──────┘       │       │           │
│      │<──────┼──────┘       │      │       │       │           │
│  ┌───┴───┐   │      │       │      │       │       │           │
│  │Display│   │      │       │      │       │       │           │
│  │  810  │   │      │       │      │       │       │           │
│  └───────┘   │      │       │      │       │       │           │
│      │       │      │       │      │       │       │           │
└──────────────┴──────────────┴──────────────┴───────────────────┘
```

---

## Diagram Requirements (USPTO)

### Formal Requirements

| Requirement | Standard |
|-------------|----------|
| Paper size | 8.5" x 11" or A4 |
| Margins | Min 1" top, 0.5" others |
| Line weight | Black, solid, consistent |
| Reference numerals | Arabic numerals (101, 102, etc.) |
| Figure labels | "FIG. 1", "FIG. 2", etc. |
| Text in drawings | Readable, horizontal preferred |

### For Provisional Applications

**Relaxed Requirements:**
- Sketches and hand drawings acceptable
- Photos can be included
- No formal shading requirements
- Reference numbers helpful but not required

> "I would rather have a bunch of sketches that are really crappy and janky than one super perfect really nice drawing." - Patent Attorney

---

## Reference Numbering Convention

| Range | Component Type |
|-------|---------------|
| 100-199 | System-level components |
| 200-299 | Hardware components |
| 300-399 | Method steps (FIG. 3) |
| 400-499 | Method steps (FIG. 4) |
| 500-599 | Data elements |
| 600-699 | Data flow elements |
| 700-799 | UI elements |
| 800-899 | Interaction elements |

---

## Description Text for Each Figure

Each figure needs accompanying description:

```markdown
## FIG. 1 - System Architecture

FIG. 1 illustrates a system 100 for [purpose], according to various embodiments.

The system 100 includes a client device 101, which may be a mobile device, desktop computer, or other computing device. The client device 101 communicates with a server 104 via a network connection 102. The network connection 102 may include the Internet, a local area network, or other communication medium.

The server 104 receives requests from the client device 101 and processes them using an ML engine 110. The ML engine 110 accesses a database 108 to retrieve necessary data for processing.

In operation, [describe how the components interact to achieve the technical result].
```

---

## Expert Guidance

### From Dylan Adams
> "Start with the figures as a base. Tell a story of how the invention works. Start at the very beginning - is it connected to the internet? How is it connected? Does it talk to a server? Are there a group of servers? What devices are involved?"

### From Software Patent Expert
> "Have a network diagram, an example interface, swim or data flow diagrams, and method diagrams. If these get too complex, break them into multiple figures. Write things in a way that makes sense to you - there's no right way or wrong way."

### From Steve Key
> "A drawing is worth a thousand words. Good line drawings that really tell the story make it easier for people to understand. Include workarounds and variations in your drawings too."

---

## Integration

After creating diagrams:
1. **provisional-patent-drafting** - Reference figures in description
2. Each figure should be referenced in detailed description
3. Reference numbers must be consistent throughout
