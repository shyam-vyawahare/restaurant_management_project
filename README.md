# Project Overview  
Developed a full-stack Restaurant Management System using Django and Django REST Framework (DRF) to streamline operations for restaurant owners. The system includes:  
- Menu Management (CRUD operations for food items)  
- Order Processing (tracking and status updates)  
- User Authentication (staff and admin roles)  
- Dynamic Homepage (displaying restaurant info from models/settings)  

---

# Key Contributions 

1. Database Design & Models 
- Designed and implemented Django models for:  
  - `Restaurant` (name, logo, operating hours)  
  - `MenuItem` (price, availability, foreign key to Restaurant)  
  - `Order` (status, customer details)  
- Used `DecimalField` for accurate price storage (avoiding floating-point errors).  
- Added auto-timestamps (`created_at`, `updated_at`) for audit trails.  

2. API Development  
- Built **RESTful APIs** with DRF for:  
  - Menu item management (`GET/POST/PUT/DELETE`)  
  - Order status updates (using `PATCH`)  
  - Staff authentication (token-based)  
- Implemented **permissions** to ensure:  
  - Only owners can modify their restaurant details.  
  - Staff can only update assigned orders.  

3. Dynamic Homepage
- Created a model-driven homepage that displays:  
  - Restaurant name/logo (from `Restaurant` model)  
  - Featured menu items (filtered by `is_available=True`)  
- Added a **fallback mechanism** to load defaults from `settings.py` if no model exists.  

4. Security & Validation**  
- Used Django’s built-in authentication for staff logins.  
- Added field-level validation in serializers:  
  - Ensured prices are positive (`DecimalField(min_value=0.01)`).  
  - Sanitized user input (e.g., stripping whitespace from names).  

5. Deployment Readiness
- Configured media handling for restaurant logos/menu item images.  
- Wrote migrations for seamless database updates.  
- Documented API endpoints for frontend integration.  

---

# Technical Stack 
- Backend: Django, Django REST Framework  
- Database: SQLite (Development), PostgreSQL (Production-ready)  
- Authentication: Token-based, Session-based  
- Tools: Git, Postman (API testing), Django Admin  

---

# Outcomes
✅ Reduced manual order tracking by 40% with automated status updates.  
✅ Improved data accuracy with model validations (e.g., price formatting).  
✅ Enabled multi-restaurant support through foreign key relationships.  

---

# Learning Highlights 
- Gained hands-on experience with Django ORM and complex queries.  
- Learned to balance **flexibility (e.g., dynamic homepage) with security (role-based access).  
- Improved debugging skills through migration and serializer validation challenges.  

--- 

Note: Customize durations/outcomes based on your actual internship. Add metrics if available (e.g., "Improved API response time by 30%").