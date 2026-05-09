# Project Context — Relevance Filter

This file helps Wanddy determine if a Discord message is relevant to the project.
Updated automatically as Wanddy learns from interactions.

## Project Identity

- **Project**: .NET 9 + React 18 enterprise application
- **Company**: jigarjoshi (.NET + React services practice)
- **Client**: <client>
- **Platform**: Linux + Docker + Nginx

## In-Scope Topics

These are RELEVANT to the project:

### Solution / Projects (our codebase)
- App.Api (ASP.NET Core Web API)
- App.Application (CQRS handlers, MediatR)
- App.Domain (entities, domain services)
- App.Infrastructure (EF Core 9, repositories, external integrations)
- App.Web (React 18 + TypeScript + Vite frontend)
- App.Tests (xUnit) and App.Web.Tests (Vitest + RTL + Playwright)

### Technologies
- .NET 9 (C# 12), ASP.NET Core 9, Entity Framework Core 9
- PostgreSQL 15+
- React 18 + TypeScript + Vite
- TanStack Query, React Router v6, Tailwind CSS / Storybook
- FluentValidation, MediatR, AutoMapper, Serilog
- Hangfire / Quartz.NET (scheduled jobs)
- Linux (Ubuntu/Debian), Docker, Nginx, systemd
- GitHub Actions (CI/CD), GHCR (container registry)
- Shopify API, ShipStation API
- REST APIs, gRPC, webhooks, message bus (RabbitMQ / Azure Service Bus)

### Business Domains
- E-commerce (Shopify integration)
- Contact management, deduplication, merging
- Sales orders, invoicing, payments
- Inventory, warehouse, shipping
- CRM, leads, opportunities
- Accounting (receivables, payables, reconciliation)

### Infrastructure
- Linux + Docker + Nginx
- GitHub: <org>/<repo>
- Branch: develop, staging, main

### Team Members
- Jigar (jig), Jin, Devz, Ali, Karm, Rita, Yash
- Any developer prefix in commit history

## Out-of-Scope Topics

These are NOT relevant — ask for clarification:

- Other tech stacks (Java/Spring, Python/Django, Rails, PHP) unless comparing
- Other client projects (unless comparing architecture)
- Personal requests, general chat
- Non-technical discussions

## Relevance Scoring

When analyzing a message, score relevance:

| Score | Meaning | Action |
|-------|---------|--------|
| **HIGH** | Mentions our solution/projects, .NET 9, React 18, Shopify, specific files/entities | Process normally |
| **MEDIUM** | General .NET / React question, could be our project or generic | Ask: "Is this for the project?" |
| **LOW** | No connection to our project, different stack | Politely redirect: "This doesn't seem related to the project. Could you provide more context about which feature or service this relates to?" |
| **ZERO** | Clearly unrelated (personal, spam, off-topic) | Acknowledge but don't process: "This channel is for the project commands. For general chat, please use another channel." |

## Keywords That Indicate Relevance

### High Confidence (definitely our project)
shopify, dedup, merge, contact, App.Api, App.Domain,
develop branch, staging branch, EF Core migration, ShipStation,
mapping, normalization, hash, duplicate, GHCR, dotnet, ef migrations, react component

### Medium Confidence (likely our project)
.NET, .net 9, asp.net core, ef core, c#, react, typescript, vite, tsx, tailwind,
controller, endpoint, dbcontext, entity, dto, mediatr, fluentvalidation, hangfire,
docker, nginx, github actions, traceback, exception, error, bug, fix, deploy, PR,
pull request

### Low Confidence (could be anything)
server, database, api, webhook, login, settings, admin, port,
test, build, release
