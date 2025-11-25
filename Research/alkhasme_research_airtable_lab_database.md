# Using Airtable as a 3D Print Lab Database  
Author: Muneer Al-Khasawneh (alkhasme)  
Course: CS 5001 – Senior Design  

## 1. What is Airtable?

Airtable is a cloud platform that mixes a spreadsheet UI with a real database underneath. It supports:
- Linked tables
- Formula fields
- Attachments
- Automations
- Multiple views and interfaces

This makes it an ideal backend for early-stage prototypes.

## 2. Why Use Airtable for PrintNet?

For v1 of PrintNet, Airtable provides:
- Easy schema creation
- Built-in UI for lab managers
- Quick integration with our backend via REST API
- Simple collaboration between team members

We can move to PostgreSQL or Firebase later if needed.

## 3. Proposed Airtable Schema

### **Users**
- Name  
- UC Username  
- Email  
- Role  
- Courses  
- Total Prints (rollup)  
- Total Filament (rollup)  
- Account Status  

### **Printers**
- Printer Name  
- Model  
- Location  
- OctoPrint URL  
- Status  
- Build Volume  
- Notes  
- Linked Jobs  

### **Print Jobs**
- Job ID  
- Submitted By  
- Model Source  
- Assigned Printer  
- Status  
- Submitted / Started / Completed timestamps  
- Estimated vs actual time  
- Material type  
- Filament (g)  
- Failure reason  
- Snapshot  

### **Materials**
- Material name  
- Type  
- Color  
- Vendor  
- Spool weight  
- Remaining weight  
- Compatible printers  

### **Presets / Profiles**
- Preset name  
- Target printer model  
- Layer height  
- Infill  
- Nozzle temp  
- Bed temp  
- Recommended usage  

## 4. Airtable Views / Interfaces

Useful views:
- Printer health dashboard  
- Active jobs list  
- Student print history  
- Material inventory  

## 5. Integration with PrintNet Backend

PrintNet can:
- Create new job records  
- Update job status from OctoPrint  
- Log failures and completions  
- Track analytics (usage per course, printer uptime, etc.)

## 6. Limitations

- Record limits (depending on plan)  
- Vendor lock-in  
- Not ideal for huge data sets  

Still, the benefits outweigh the drawbacks for v1.
