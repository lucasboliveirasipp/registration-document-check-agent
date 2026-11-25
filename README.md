# Registration Document Check Agent

Checks ownership-transfer and registration forms for capitalization bonds against the supporting documents of individuals, companies and assignees: it reads the form, finds each person's documents and scores whether names, tax IDs and signatures match.

**Stack:** Python · Streamlit · Azure Document Intelligence (form fields and signatures) · Azure OpenAI · typed domain models
**Role:** Lead developer: design and implementation
**Related:** [Document Verification API](https://github.com/lucasboliveirasipp/document-verification-api), a production API for registration-document checks

> Built at a large Brazilian insurer. The company is replaced by the fictional **Acme Seguros**, and every name, document and data point here is fictional. Code, prompts and UI are in Portuguese, written for Brazilian business teams.

## Problem

Transferring a capitalization bond from one holder to another needs a signed form plus IDs, proofs of address, bank details and, for companies, articles of association and legal representatives. Analysts compared all of it by hand.

## What I built

- **Three flows:** individual (PF), company (PJ) and assignee.
- **Form extraction** with Document Intelligence: field values and signature presence for subscriber, current holder and new holder.
- **Document matching by tax ID (CPF/CNPJ):** each person on the form is matched to their documents, then names are compared with accent-insensitive similarity scores instead of exact equality.
- **Domain model** for the product (bond, holder, subscriber, payment and signature types) so every rule is explicit in code.
- The LLM reads unstructured documents; the comparisons and scores are computed in Python.

## Run it

```bash
python -m venv .venv && .venv\Scripts\activate   # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                               # Azure OpenAI + Document Intelligence
streamlit run streamlit_app.py
```

Use fictional sample forms and documents.

---
Part of my [AI engineering portfolio](https://github.com/lucasboliveirasipp).
