# Folder Structure & Workspace Templates

Use this reference to generate the appropriate directory layout based on project size, programming language, and framework choice.

---

## 1. Node.js & TypeScript Templates

### A. Small Size (Flat/Single-purpose)
* **Target**: Landing page, lightweight server, microservice, or simple API.
* **Layout**:
```text
project-root/source/
├── src/
│   ├── index.ts          # Entry point
│   ├── config.ts         # Environment variables & constants
│   ├── routes.ts         # API Route definitions
│   ├── db.ts             # Simple DB client (Prisma/pg)
│   └── utils.ts          # Helper functions
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
└── README.md
```

### B. Medium Size (MVC / Layered)
* **Target**: Standard web API with database, user auth, and multiple domains.
* **Frameworks**: Express, NestJS (Standard), Fastify.
* **Layout**:
```text
project-root/source/
├── src/
│   ├── config/           # Database configurations, CORS, constants
│   ├── controllers/      # Request handlers & validators
│   ├── middlewares/      # Auth gates, error handlers, logging
│   ├── models/           # DB schema representations (Prisma/Mongoose/TypeORM)
│   ├── routes/           # Router dispatchers (auth.ts, users.ts)
│   ├── services/         # Business logic layer
│   ├── utils/            # Helper utilities
│   └── app.ts            # App startup and middleware mounting
├── tests/                # Unit & Integration test suites
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
└── README.md
```

### C. Large Size (Monorepo Workspace)
* **Target**: Enterprise applications with web client, admin panel, backend API, and shared logic.
* **Frameworks**: Next.js (FE), Express/NestJS (BE), npm/yarn/pnpm Workspaces, Turborepo.
* **Layout**:
```text
project-root/source/
├── apps/
│   ├── web/              # Frontend client (Next.js/Vite)
│   │   ├── src/
│   │   │   ├── app/      # Next.js App Router (pages & layouts)
│   │   │   ├── components/ # Reusable UI components
│   │   │   └── hooks/    # React custom hooks
│   │   └── package.json
│   └── api/              # Backend server (Express/NestJS)
│       ├── src/
│       │   ├── modules/  # Modular domains (Auth, Users, Products)
│       │   └── main.ts   # Entrypoint
│       └── package.json
├── packages/             # Shared packages
│   ├── db/               # Prisma database schemas, migrations & client
│   │   ├── prisma/
│   │   │   └── schema.prisma
│   │   └── package.json
│   ├── ui/               # Shared UI component library (Tailwind/Radix)
│   │   └── package.json
│   └── tsconfig/         # Shared TypeScript configurations
├── docker-compose.yml
├── turbo.json            # Monorepo task runner configuration
├── package.json          # Root package workspace definitions
└── README.md
```

---

## 2. Rust Templates

### A. Small Size (Flat Crate)
* **Target**: CLI utility, simple daemon, single binary.
* **Layout**:
```text
project-root/source/
├── src/
│   ├── main.rs           # CLI Parser & Entry point
│   ├── commands.rs       # Command handlers
│   └── utils.rs          # Formatters, spinners
├── Cargo.toml
├── LICENSE
└── README.md
```

### B. Medium Size (Layered Single Crate)
* **Target**: Web server API with SQLx.
* **Frameworks**: Axum, Actix-web, Rocket.
* **Layout**:
```text
project-root/source/
├── src/
│   ├── config.rs         # Environment configs
│   ├── routes/           # Router modules (users.rs, auth.rs)
│   ├── controllers/      # Endpoint handlers
│   ├── models/           # Struct definitions (DB rows, DTOs)
│   ├── services/         # Core business operations
│   ├── db.rs             # Database pool setup
│   ├── errors.rs         # Custom error enum and responder impl
│   └── main.rs           # Startup & listener binding
├── tests/                # Integration tests
├── migrations/           # SQLx migration scripts
├── Cargo.toml
├── .env.example
└── README.md
```

### C. Large Size (Cargo Workspace Monorepo)
* **Target**: Complex systems with an API server, database migrator crate, and background batch jobs.
* **Layout**:
```text
project-root/source/
├── Cargo.toml            # Root Cargo Workspace definition
├── Cargo.lock
├── crates/
│   ├── api-server/       # Axum API binary
│   │   ├── src/
│   │   │   ├── routes/
│   │   │   └── main.rs
│   │   └── Cargo.toml
│   ├── batch-processor/  # Batch processing pipeline binary
│   │   ├── src/
│   │   │   ├── pipeline/
│   │   │   └── main.rs
│   │   └── Cargo.toml
│   ├── core-domain/      # Shared domain logic & models (library)
│   │   ├── src/
│   │   │   ├── entities.rs
│   │   │   └── repository.rs
│   │   └── Cargo.toml
│   └── db-adapter/       # Database queries & connection pools (library)
│       ├── src/
│       │   └── lib.rs
│       └── Cargo.toml
├── migrations/           # Shared database migration scripts
├── docker-compose.yml
└── README.md
```

---

## 3. Python Templates

### A. Small Size (Flat Script/API)
* **Target**: Simple script, ETL, or single-file Flask/FastAPI server.
* **Layout**:
```text
project-root/source/
├── main.py               # Application entry point
├── config.py             # Environment configurations
├── requirements.txt
├── .env.example
└── README.md
```

### B. Medium Size (Modular Layered)
* **Target**: FastAPI application with SQL Alchemy or Tortoise ORM.
* **Layout**:
```text
project-root/source/
├── app/
│   ├── api/              # API endpoints / routers
│   │   ├── v1/
│   │   │   ├── endpoints/ # auth.py, users.py
│   │   │   └── router.py  # Mount endpoints
│   │   └── deps.py        # Database and auth dependencies
│   ├── core/             # Configuration, security, logging settings
│   ├── db/               # Database session, base model
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas (validation/DTOs)
│   ├── services/         # Business operations logic
│   └── main.rs           # FastAPI app instance and startup events
├── tests/                # Pytest suites
├── alembic/              # Database migration environments
├── alembic.ini
├── requirements.txt
├── .env.example
└── README.md
```

### C. Large Size (Clean Architecture / DDD)
* **Target**: Enterprise applications with highly decoupled business domain.
* **Layout**:
```text
project-root/source/
├── src/
│   ├── domain/           # Enterprise domain rules (no DB/API deps)
│   │   ├── entities/     # Domain objects
│   │   └── interfaces/   # Abstract repository definitions
│   ├── application/      # Orchestrates domain logic
│   │   ├── use_cases/    # create_user.py, update_product.py
│   │   └── dtos/         # Input/Output data structures
│   ├── infrastructure/   # Technical details (frameworks, DB, HTTP)
│   │   ├── db/           # ORM engine, repository implementations
│   │   ├── external_apis/# Integrations (Stripe, Twilio)
│   │   └── security/     # JWT, hashing
│   └── presentation/     # HTTP/CLI endpoints interface
│       ├── rest/         # FastAPI/Flask routes
│       └── cli/          # Click/Argparse definitions
├── tests/                # Unit, Integration, E2E tests
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 4. Go Templates

### A. Small Size (Flat Package)
* **Target**: Simple daemon, CLI command.
* **Layout**:
```text
project-root/source/
├── main.go               # Entry point
├── config.go             # Simple configs
├── go.mod
├── go.sum
└── README.md
```

### B. Medium/Large Size (Standard Go Project Layout - `/cmd` and `/internal`)
* **Target**: Medium to large Go microservices.
* **Standard**: Follows `golang-standards/project-layout`.
* **Layout**:
```text
project-root/source/
├── cmd/
│   ├── api-server/       # Executable entrypoint for API
│   │   └── main.go
│   └── batch-worker/     # Executable entrypoint for batch job
│       └── main.go
├── internal/             # Private application code (cannot be imported externally)
│   ├── config/           # App configurations
│   ├── domain/           # Core domain definitions & models
│   ├── handler/          # HTTP handlers (Gin/Fiber/mux router)
│   ├── middleware/       # JWT auth, recovery, logger middlewares
│   ├── repository/       # GORM or sqlx query implementations
│   └── service/          # Business logic orchestrators
├── pkg/                  # Shared public libraries (can be imported by other projects)
│   └── logger/           # Logging wrappers
├── api/                  # Swagger or OpenAPI specifications
├── deployments/          # Dockerfile, Helm charts
├── go.mod
├── go.sum
└── README.md

---

## 5. Java & Spring Boot Templates

### A. Standard Size (Layered MVC)
* **Target**: Enterprise REST APIs and microservices.
* **Layout**:
```text
project-root/source/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── company/
│   │   │           └── app/
│   │   │               ├── config/       # Security, Beans, WebMvcConfigurer
│   │   │               ├── controller/   # REST endpoints
│   │   │               ├── dto/          # Data Transfer Objects
│   │   │               ├── exception/    # Global exception handlers
│   │   │               ├── model/        # JPA Entities
│   │   │               ├── repository/   # Spring Data Repositories
│   │   │               ├── service/      # Business logic
│   │   │               └── Application.java # Main class
│   │   └── resources/
│   │       ├── application.yml   # Properties & profiles
│   │       └── db/migration/     # Flyway or Liquibase scripts
│   └── test/                     # JUnit and Mockito tests
├── pom.xml                       # Maven (or build.gradle for Gradle)
└── README.md
```

---

## 6. C# & .NET Templates

### A. Standard Web API (Clean Architecture)
* **Target**: Enterprise Web API.
* **Layout**:
```text
project-root/source/
├── src/
│   ├── Api/                      # ASP.NET Core Web API project (Controllers, Program.cs)
│   ├── Application/              # Use cases, MediatR handlers, DTOs, interfaces
│   ├── Domain/                   # Entities, Enums, Exceptions, value objects
│   └── Infrastructure/           # EF Core DbContext, migrations, external API clients
├── tests/
│   ├── Api.IntegrationTests/
│   └── Application.UnitTests/
├── MySolution.sln
└── README.md
```

---

## 7. Frontend Templates (Standalone)

### A. React / Vue (Vite)
* **Target**: Single Page Applications (SPA).
* **Layout**:
```text
project-root/source/
├── src/
│   ├── assets/           # Static files (images, fonts)
│   ├── components/       # Reusable UI components
│   ├── features/         # Feature-based modules (domain logic + UI)
│   ├── hooks/            # Custom React/Vue hooks
│   ├── layouts/          # Page wrappers (e.g., DashboardLayout)
│   ├── pages/            # Routable screen components
│   ├── store/            # Global state (Zustand, Redux, Pinia)
│   ├── utils/            # Helper functions
│   ├── App.tsx           # Root component
│   └── main.tsx          # DOM mounting
├── public/               # Favicon, robots.txt
├── index.html            # Vite HTML entry
├── vite.config.ts
├── package.json
└── README.md
```

### B. Next.js (App Router)
* **Target**: Fullstack React apps, SSR/SSG.
* **Layout**:
```text
project-root/source/
├── src/
│   ├── app/              # App Router (pages, layouts, api routes)
│   │   ├── (auth)/       # Route groups
│   │   ├── api/          # Next.js API routes
│   │   ├── layout.tsx    # Root layout
│   │   └── page.tsx      # Home page
│   ├── components/       # Shared UI components
│   ├── lib/              # Utility functions, DB clients, generic configs
│   └── styles/           # Global CSS, Tailwind base
├── public/               # Static assets
├── next.config.js
├── tailwind.config.js
├── package.json
└── README.md
```
