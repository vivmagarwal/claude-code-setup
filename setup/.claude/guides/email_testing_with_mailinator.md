# Email Testing with Mailinator

## What is Mailinator?

Mailinator provides free, public email inboxes. Any email sent to `anything@mailinator.com` can be viewed without authentication - perfect for testing email-based features.

## How to Use

1. **Create a test email**: Pick any name, e.g., `myapp-test-123@mailinator.com`

2. **Use in your app**: Enter this email in signup, forgot-password, or any email-requiring form

3. **Check the inbox**:
   ```
   https://www.mailinator.com/v4/public/inboxes.jsp?to=myapp-test-123
   ```

4. **View email content**: Click on the email, use the "LINKS" tab to find clickable URLs

5. **Test the flow**: Click verification/reset links to complete the flow

## Example: Testing Signup Flow

```bash
# 1. Go to your app's signup page
http://localhost:3000/signup

# 2. Enter test email
myapp-test-2026@mailinator.com

# 3. Check inbox
https://www.mailinator.com/v4/public/inboxes.jsp?to=myapp-test-2026

# 4. Click the verification email
# 5. Use LINKS tab to find confirmation URL
# 6. Click link to complete verification
```

## Example: Testing Password Reset

```bash
# 1. Go to forgot password page
http://localhost:3000/forgot-password

# 2. Enter test email (must be registered)
myapp-test-2026@mailinator.com

# 3. Check inbox for password reset email
# 4. Click reset link from LINKS tab
# 5. Set new password on reset-password page
```

## Tips

- Mailinator inboxes are **public** - never use for sensitive data
- Emails arrive within seconds
- Use unique inbox names per test run (e.g., include timestamp)
- The LINKS tab makes it easy to find action URLs without parsing HTML

## Alternative Services

- [Guerrilla Mail](https://www.guerrillamail.com/)
- [10 Minute Mail](https://10minutemail.com/)
- [Temp Mail](https://temp-mail.org/)
- [Mailtrap](https://mailtrap.io/) - for staging/dev environments with team access
