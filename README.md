# Student Grade Tracker 

A modular, Python-based CLI application for managing student academic records, generating insights, and producing text-based report cards.  

---

## **Overview**
The **Student Grade Tracker** is a command-line application designed to help users:

- Manage student records  
- Compute academic metrics  
- Generate class-level and subject-level analytics  
- Create text-based report cards  
- Cleanly separate logic, UI, utilities, and business rules  

The project follows **industry-standard modular architecture**, making it easy to extend, maintain, and understand.

---

## **Features**

### Student Search
- Search by **Student ID**
- Search by **Full Name**
- Filter students by **Grade**
- Display **Top N Students**

### Metrics & Analytics
- Total, percentage, grade calculation  
- Class average percentage  
- Grade distribution  
- Pass/fail counts  
- Subject-wise average  
- Subject hardest/easiest identification  

### CRUD Operations
- Update student (with full metrics recalculation)  
- Delete student (safe removal + recalculation)

### Report Cards
- Generates professional text-based report cards
- Stored inside `/data/report_cards`
- Includes subject scores, totals, percentage, rank

### JSON File Input
- Load student data from JSON  
- Processed data generated dynamically  
- Safe validation

---

## **Project Architecture**

This project follows a **3-layer clean architecture**:

- UI Layer → Handles printing & user interaction (menu, display)
- Service Layer → Pure logic (search, update, delete, metrics, stats)
- Utils Layer → Validation, JSON I/O, constants

---

## **Technologies & Concepts Used**

### Python Concepts:
- Functions & modular programming  
- File handling with JSON  
- Dictionaries, lists, comprehensions  
- Generators  
- Exception-safe validation  
- In-place list updates  
- Clean architecture design  

### Data Processing Concepts:
- Ranking logic  
- Aggregations  
- Subject-wise analytics  
- Mean, min, max calculations  
- Pass/fail evaluation with compound conditions  


