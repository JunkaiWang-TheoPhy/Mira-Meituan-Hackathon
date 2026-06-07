# dining-skill

Mira uses this skill when the user is likely to need a meal but has not asked
for a generic restaurant search. The skill combines recent state, dislikes,
budget, weather, and delivery ETA into one confirmable meal proposal.

## Trigger Events

- `meal_risk_detected`

## Tool Surface

- `inferMealNeed(context)`
- `searchDiningCandidates(location, preferences)`
- `filterByRestrictions(candidates, allergies, disliked, recentMeals)`
- `rankByState(candidates, heartState, workStatus, weather, budget)`
- `createMealOrderPreview(candidate)`
- `confirmMealOrder(orderPreviewId)`
