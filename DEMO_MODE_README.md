# Developer Mode & Test Email Management

This document describes the developer mode and test email management features built into the job search analytics application. Developer mode allows users to work with the full application flow using mock Gmail API data instead of real emails.

## Overview

The application includes a comprehensive developer mode system that allows users to:
1. **Developer Mode**: Use mock Gmail API calls with test emails instead of real Gmail data
2. **Test Email Management**: Add, edit, delete, and categorize test emails for testing and development
3. **Full Application Flow**: All functions work exactly like the real app, just with mock data
4. **Automatic Setup**: Developer mode infrastructure is automatically available when the app starts

## Features

### Developer Mode

- **Toggle Developer Mode**: Switch between real Gmail API and mock Gmail API via UI
- **Development Safe**: No real email data is accessed when using mock API
- **Realistic Test Data**: Pre-loaded with realistic job application emails
- **Full Application Flow**: All functions work exactly like the real app
- **Always Available**: Infrastructure is always ready, toggle as needed

### Test Email Management

- **Add Custom Emails**: Create new test emails with full email body content
- **Search & Filter**: Search through test emails by company, subject, or content
- **Categorization**: Organize emails by categories (rejection, interview, etc.)
- **Edit & Delete**: Modify existing test emails or remove them
- **Demo vs Custom**: Distinguish between demo emails and user-created emails

## Usage

### Enabling Developer Mode

1. **UI Toggle**: Click the "Dev Mode" toggle in the navbar (only visible on dashboard)
2. **Via Test Email Manager**: Use the "Manage Test Emails" button on the dashboard
3. **Runtime Control**: Toggle between real and mock Gmail API at any time

### Managing Test Emails

1. Click "Manage Test Emails" on the dashboard
2. Use the interface to:
   - Add new test emails
   - Search existing emails
   - Edit email details
   - Delete emails
   - Toggle demo mode

### Adding Test Emails

1. Click "Add Test Email" in the Test Email Manager
2. Fill in the required fields:
   - Company Name
   - Application Status (dropdown with predefined options)
   - Job Title
   - Subject
   - From Email
   - Email Body (full content)
   - Category (optional)
   - Notes (optional)

## Technical Implementation

### Backend

- **New Database Table**: `test_emails` for storing test email data
- **New Routes**: `/test-emails/*` endpoints for CRUD operations
- **Mock Gmail Service**: Complete mock implementation of Gmail API
- **Developer Mode Integration**: Modified email routes to use mock service when developer mode is toggled
- **Session-based Toggle**: Developer mode state stored in user session

### Frontend

- **TestEmailManager Component**: Full-featured UI for managing test emails
- **DemoModeToggle Component**: Simple toggle for developer mode in navbar
- **Integration**: Seamlessly integrated with existing dashboard

### Database Schema

```sql
CREATE TABLE test_emails (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR PRIMARY KEY,
    company_name VARCHAR NOT NULL,
    application_status VARCHAR NOT NULL,
    received_at TIMESTAMP NOT NULL,
    subject VARCHAR NOT NULL,
    job_title VARCHAR NOT NULL,
    email_from VARCHAR NOT NULL,
    email_body TEXT NOT NULL,
    is_demo_email BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    category VARCHAR,
    tags VARCHAR,
    notes TEXT
);
```

## Getting Started

### Quick Start

The developer mode infrastructure is automatically set up when you start the application:

```bash
# Start the application with Docker Compose
docker-compose up

# The application will automatically:
# 1. Set up the database and tables
# 2. Load demo emails for testing
# 3. Start all services
# 4. Be ready to use with developer mode toggle
```

### Manual Setup (if needed)

If you need to manually set up the environment:

```bash
# Set up with default user
python backend/scripts/dev_setup.py

# Set up with custom user ID
python backend/scripts/dev_setup.py my_user_123

# List demo emails
python backend/scripts/dev_setup.py --list

# Clear demo data
python backend/scripts/dev_setup.py --clear
```

## Configuration

### Environment Variables

Add to your `.env` file:
```
DEMO_MODE=false  # Enable demo mode globally (optional)
```

### Demo Email Data

The system comes pre-loaded with realistic demo emails including:
- Application confirmations
- Interview invitations
- Rejections
- Assessment requests
- Offer letters
- And more...

## API Endpoints

### Test Email Management
- `GET /test-emails` - Get all test emails for user
- `POST /add-test-email` - Add new test email
- `PUT /update-test-email/{id}` - Update existing test email
- `DELETE /delete-test-email/{id}` - Delete test email
- `GET /search-test-emails?q={query}` - Search test emails
- `GET /test-email-categories` - Get available categories

### Demo Mode
- `POST /enable-demo-mode` - Enable demo mode and load demo emails
- `POST /disable-demo-mode` - Disable demo mode

## Benefits

### For Live Presentations
- **Privacy**: No real email data exposed
- **Consistency**: Same data every time
- **Control**: Predictable outcomes for demos

### For Development
- **Testing**: Comprehensive test data for development
- **Debugging**: Easy to reproduce specific scenarios
- **Feature Development**: Test new features without real data

### For Contributors
- **Easy Setup**: Quick way to add test cases
- **Categorization**: Organize test data by type
- **Search**: Find specific test scenarios quickly

## Migration

To set up the new features:

1. **Database Migration**: Run the new migration for the `test_emails` table
2. **Environment Setup**: Add `DEMO_MODE` to your environment variables (optional)
3. **Restart Services**: Restart backend and frontend services

## Future Enhancements

Potential improvements:
- **Bulk Import**: Import test emails from CSV/JSON
- **Export**: Export test email collections
- **Templates**: Pre-built email templates
- **Sharing**: Share test email collections between users
- **Versioning**: Track changes to test emails over time 