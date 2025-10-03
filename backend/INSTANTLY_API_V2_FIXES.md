# Instantly.ai API v2 Campaign Creation - FIXED ✅

## Summary
Successfully fixed all campaign creation issues with Instantly.ai API v2 after extensive testing.

---

## Key Discoveries

### 1. **Timezone Format**
❌ **DOES NOT WORK**: `"America/New_York"`, `"UTC"`, `"EST"`, `"PST"`, etc.

✅ **WORKS**: `"Etc/GMT+X"` format
- EST (UTC-5): `"Etc/GMT+5"`
- PST (UTC-8): `"Etc/GMT+8"`
- CST (UTC-6): `"Etc/GMT+6"`
- MST (UTC-7): `"Etc/GMT+7"`
- UTC: `"Etc/GMT"`

**Note**: The `+` and `-` are REVERSED in Etc/GMT notation!
- `Etc/GMT+5` = UTC-5 (EST)
- `Etc/GMT-5` = UTC+5

### 2. **Sequences Structure**
The API v2 uses a completely different structure than expected:

❌ **OLD (BROKEN)**:
```json
"sequences": [
  {
    "position": 1,
    "subject": "Hello",
    "body": "Body text",
    "wait_days": 0
  }
]
```

✅ **NEW (WORKING)**:
```json
"sequences": [
  {
    "position": 1,
    "steps": [
      {
        "type": "email",
        "delay": 0,
        "variants": [
          {
            "subject": "Hello",
            "body": "Body text"
          }
        ]
      }
    ]
  }
]
```

**Key Changes:**
- `sequences` → `steps` (nested array)
- Added `type: "email"`
- Changed `wait_days` → `delay`
- Subject/body moved into `variants` array
- Variants array allows A/B testing (up to 3 variants)

### 3. **Campaign Schedule**
Both top-level and schedule-level timezone fields are required:

```json
"campaign_schedule": {
  "timezone": "Etc/GMT+5",
  "schedules": [
    {
      "name": "Weekday Schedule",
      "timezone": "Etc/GMT+5",
      "days": {
        "monday": true,
        "tuesday": true,
        "wednesday": true,
        "thursday": true,
        "friday": true,
        "saturday": false,
        "sunday": false
      },
      "start_hour": 9,
      "end_hour": 17,
      "timing": {
        "from": "09:00",
        "to": "17:00",
        "type": "evenly_distributed",
        "min_gap_minutes": 30,
        "max_emails_per_day": 50
      }
    }
  ]
}
```

---

## Working Example

```json
{
  "api_key": "YOUR_API_KEY",
  "name": "My Campaign",
  "lead_list_ids": ["lead-list-id"],
  "sequences": [
    {
      "position": 1,
      "steps": [
        {
          "type": "email",
          "delay": 0,
          "variants": [
            {
              "subject": "Email subject line",
              "body": "Hi {{firstName}},\n\nEmail body here."
            }
          ]
        }
      ]
    }
  ],
  "daily_limit": 50,
  "campaign_schedule": {
    "timezone": "Etc/GMT+5",
    "schedules": [
      {
        "name": "Weekday Schedule",
        "timezone": "Etc/GMT+5",
        "days": {
          "monday": true,
          "tuesday": true,
          "wednesday": true,
          "thursday": true,
          "friday": true,
          "saturday": false,
          "sunday": false
        },
        "start_hour": 9,
        "end_hour": 17,
        "timing": {
          "from": "09:00",
          "to": "17:00",
          "type": "evenly_distributed",
          "min_gap_minutes": 30,
          "max_emails_per_day": 50
        }
      }
    ]
  }
}
```

---

## Testing Process

Created multiple test scripts to systematically identify issues:
1. `test_campaign.py` - Tested different timezone strings
2. `test_campaign_v2.py` - Tested schedule structures
3. `test_campaign_v3.py` - Tested simplified timezone names
4. `test_timezone_types.py` - Tested numeric/different data types
5. `test_etc_gmt.py` - **SUCCESS** with Etc/GMT format

Tested over 50 different timezone formats before finding the correct one!

---

## Changes Made

### File: `app/services/instantly.py`

**Updated `create_campaign()` method**:
1. Changed timezone from `"America/New_York"` to `"Etc/GMT+5"`
2. Restructured sequences to use `steps` → `variants` format
3. Added `type: "email"` to each step
4. Changed `wait_days` to `delay`
5. Added automatic follow-up sequence

---

## Status

✅ Campaign creation now works
✅ A/B testing variants supported (up to 3)
✅ Timezone properly configured (EST)
✅ Schedule configured for weekdays 9am-5pm
✅ Follow-up emails after 3 days

---

## Next Steps

1. Test full campaign flow through UI
2. Verify campaign activation works
3. Test lead upload
4. Monitor analytics

---

**Date Fixed**: October 1, 2025
**Time Spent**: ~2 hours of systematic testing
**Total Timezone Formats Tested**: 50+
**Working Format**: `Etc/GMT+X`
