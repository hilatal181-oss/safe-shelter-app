
import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

# עיצוב דף האתר
st.set_page_config(page_title="SafeRoute", page_icon="🛡️")
st.title("🛡️ SafeRoute - ניווט בזמן אמת")
st.write("מציאת המרחב המוגן הקרוב ביותר למסלול שלך")

# מאגר המקלטים (ה-Database שלנו)
shelters = [
    {"name": "מקלט אילת 40", "lat": 31.9860, "lon": 34.7720},
    {"name": "ביח וולפסון", "lat": 32.0230, "lon": 34.7610},
    {"name": "תחנת דלק סיירים", "lat": 32.0080, "lon": 34.8250},
    {"name": "קניון עזריאלי חולון", "lat": 32.0080, "lon": 34.7730}
]

# תיבת הקלט למשתמש - כאן קורה הקסם!
user_dest = st.text_input("לאן את נוסעת?", placeholder="הקלידי יעד (למשל: תל אביב, חולון)...")

if user_dest:
    # נקודת מוצא (כרגע סימולציה למרכז חולון)
    start_pos = [31.988, 34.775] 
    
    # יצירת המפה
    m = folium.Map(location=start_pos, zoom_start=14)
    
    # אלגוריתם מציאת המקלט הקרוב ביותר
    closest = min(shelters, key=lambda s: geodesic(start_pos, (s['lat'], s['lon'])).meters)
    dist = geodesic(start_pos, (closest['lat'], closest['lon'])).meters
    
    # הוספת סמנים למפה
    folium.Marker(start_pos, popup="המיקום שלך", icon=folium.Icon(color='blue', icon='car', prefix='fa')).add_to(m)
    folium.Marker([closest['lat'], closest['lon']], popup=closest['name'], icon=folium.Icon(color='red', icon='star', prefix='fa')).add_to(m)
    folium.PolyLine([start_pos, [closest['lat'], closest['lon']]], color="red", weight=4, dash_array='5,5').add_to(m)
    
    # הצגת המפה באתר
    st_folium(m, width=700, height=500)
    
    # הודעת הצלחה למשתמש
    st.success(f"נמצא מקלט קרוב! סעי ל{closest['name']} (מרחק: {int(dist)} מטרים)")
