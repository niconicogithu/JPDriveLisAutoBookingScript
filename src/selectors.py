"""
CSS selectors for the Kanagawa e-Shinsei website.

Based on actual HTML structure from the facility selection page.
"""

# Consent checkbox (must be checked before selecting slots)
# Note: The checkbox is hidden, wrapped in a label. Click the label to check it.
CONSENT_CHECKBOX = "input#reserveCaution[type='checkbox']"
CONSENT_CHECKBOX_LABEL = "label[for='reserveCaution']"

# Main table structure
SLOT_TABLE = "table#TBL.time--table"

# Table header row with dates (format: "01/18<br>(Sun)")
DATE_HEADER_ROW = "tr#height_headday"
DATE_HEADER_CELLS = "tr#height_headday td.time--table.time--th--date"

# Category rows (each row represents a 予約枠名 like 普通車ＡＭ, 準中型車ＡＭ, etc.)
# Row IDs follow pattern: height_auto_{category_name}
CATEGORY_ROW_PREFIX = "tr[id^='height_auto_']"

# Slot cell states
SLOT_CELLS = {
    # Available slot (green circle, clickable)
    "available": "td.time--table.time--th--date.tdSelect.enable",
    
    # Unavailable slot (red X)
    "unavailable": "td.time--table.time--th--date.disable",
    
    # Out of period (gray dash)
    "out_of_period": "td.time--table.time--th--date.time--cell--tri.none",
}

# Available slot link (inside available cells)
AVAILABLE_SLOT_LINK = "a.enable.nooutline"

# SVG icons for visual identification
SVG_ICONS = {
    # Green circle (○) - available
    "available": "svg[aria-label='予約可能']",
    
    # Red X (×) - unavailable
    "unavailable": "svg[aria-label='空き無']",
    
    # Gray dash (－) - out of period
    "out_of_period": "svg[aria-label='時間外']",
    
    # Checkmark (✓) - selected
    "selected": "svg[aria-label='選択中']",
}

# Category name selector (th element in each row)
CATEGORY_NAME_CELL = "th.time--table.time--th.main_color"

# Facility name (first th in the table, spans multiple rows)
FACILITY_NAME_CELL = "th.time--table.time--th[rowspan]"


# Time selection page selectors (after clicking a slot)
TIME_SELECTION = {
    "radio_buttons": "input[type='radio']",
    "time_slots": "input[type='radio'][name*='time']",
    "submit_button": "input[type='submit'], button[type='submit']",
}

# Reservation confirmation button
RESERVATION_BUTTON = [
    "button:has-text('予約')",
    "input[type='submit'][value*='予約']",
    "button[type='submit']",
]
