# Authentication ID Resolution Strategy

## Current Issue
The codebase has a mismatch between hardcoded demo IDs and the actual database schema that expects UUIDs from authentication.

### Database Schema Expected IDs:
- **users.id**: UUID from auth.users (Supabase/Firebase Auth)
- **parents.id**: UUID generated, linked via parents.user_id
- **kids.id**: UUID generated, linked via kids.parent_id
- **stories.kid_id**: References kids.id

### Current Hardcoded IDs in Code:
- `demo_child_123` - Used in frontend for story creation
- `demo_parent_456` - Potentially used for parent dashboard
- `default` - Used as fallback in voice upload

## Resolution Strategy

### 1. During Authentication Setup:
When implementing Firebase/Supabase auth, update these files:

#### Frontend Changes:
- `/app/(kids)/kids/type/page.tsx`: Replace `demo_child_123` with actual child ID from auth context
- `/app/(kids)/kids/record/page.tsx`: Replace `demo_child_123` with actual child ID from auth context
- `/app/(parents)/parents/dashboard/page.tsx`: Replace `demo_child_123` with actual child ID from parent's children list

#### Backend Changes:
- Add middleware to extract user ID from auth token
- Map auth user ID to appropriate child/parent ID in database queries
- Update API endpoints to validate user has access to requested child data

### 2. Migration Path:
```sql
-- Create demo users for development
INSERT INTO public.users (id, email, role, full_name) VALUES
  ('11111111-1111-1111-1111-111111111111', 'demo@parent.com', 'parent', 'Demo Parent'),
  ('22222222-2222-2222-2222-222222222222', 'demo@child.com', 'kid', 'Demo Child');

INSERT INTO public.parents (id, user_id) VALUES
  ('demo_parent_456', '11111111-1111-1111-1111-111111111111');

INSERT INTO public.kids (id, user_id, parent_id, name, age) VALUES
  ('demo_child_123', '22222222-2222-2222-2222-222222222222', 'demo_parent_456', 'Demo Kid', 7);
```

### 3. Auth Context Implementation:
```typescript
// contexts/AuthContext.tsx
interface AuthContextType {
  user: User | null;
  childId: string | null; // Current active child for parents
  isParent: boolean;
  isKid: boolean;
}

// For kids: childId = their own ID from kids table
// For parents: childId = selected child from their children list
```

### 4. API Endpoint Updates:
All endpoints should:
1. Extract user ID from auth token
2. Verify user has permission to access requested resources
3. For parents: Check child belongs to them via parent_id
4. For kids: Check they're accessing their own data

### 5. Key Considerations:
- Keep demo IDs for development/testing
- Add environment flag to toggle between demo and real auth
- Ensure all foreign key constraints are satisfied
- Update RLS policies to use actual auth.uid() instead of hardcoded IDs

## Testing Checklist:
- [ ] Parent can only see their own children
- [ ] Kids can only create stories for themselves
- [ ] Stories are properly linked to kids table
- [ ] Emotion alerts are visible to correct parent
- [ ] Session data uses correct child IDs