import http.server
import json
import os
import pandas as pd

class LiveDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 1. CHANGE THIS LINE: Use .startswith() instead of == so it catches the ?region= filter parameters
        if self.path.startswith('/api/live-data'):
            try:
                csv_path = 'outputs/cleaned_customer_dataset.csv'
                
                # 2. PARSE THE REGION PARAMETER RIGHT HERE
                from urllib.parse import urlparse, parse_qs
                parsed_url = urlparse(self.path)
                query_params = parse_qs(parsed_url.query)
                selected_region = query_params.get('region', [None])[0]

                # 3. Read your data frame
                import pandas as pd
                df = pd.read_csv(csv_path)

                # 4. FILTER THE DATAFRAME IF A REGION IS SELECTED
                if selected_region and selected_region != "ALL":
                    region_mapping = {
                        "APAC": "APAC",
                        "Africa": "EMEA",
                        "Europe": "EU",
                        "LATAM": "LATAM",
                        "USCA": "US" # Maps the dropdown option seamlessly to the dataset text
                    }
                    target_string = region_mapping.get(selected_region, selected_region)
                    
                    # Uses the strict Market column descriptor to execute the dataframe slice filter
                    df = df[df['Market'] == target_string]

                # ... Leave the rest of your calculations exactly the same, just make sure they use 'df' ...
                def get_clean_col(names, fallback):
                    for c in df.columns:
                        if c.lower().strip() in [n.lower() for n in names]:
                            return c
                    return fallback

                # 1. DEFINE COLUMN SCHEMAS (Fixes NameError)
                sales_c = 'Sales'
                profit_c = 'Profit'
                order_c = 'Order ID'
                cust_c = 'Customer ID'
                cust_name_c = 'Customer Name'
                prod_name_c = 'Product Name'
                cat_c = 'Category'
                country_c = 'Country'
                market_c = 'Market'

                # Clean numeric values to ensure calculations parse smoothly
                df[sales_c] = pd.to_numeric(df[sales_c].astype(str).str.replace(r'[^\d.-]', '', regex=True), errors='coerce').fillna(0)
                df[profit_c] = pd.to_numeric(df[profit_c].astype(str).str.replace(r'[^\d.-]', '', regex=True), errors='coerce').fillna(0)

                # 2. Extract Key Baseline KPIs
                total_sales = float(df[sales_c].sum())
                total_orders = int(df[order_c].nunique())
                aov = total_sales / total_orders if total_orders > 0 else 0
                total_customers = int(df[cust_c].nunique())
                
                # 3. Process Real Top 5 Best-Selling Products directly from file
                raw_top_prods = df.groupby(prod_name_c)[sales_c].sum().sort_values(ascending=False).head(5)
                top_products_mapped = {str(k): float(v) for k, v in raw_top_prods.items()}
                
                # 4. Process Real Top 5 Elite Customer Names directly from file
                raw_top_custs = df.groupby(cust_name_c)[sales_c].sum().sort_values(ascending=False).head(5)
                top_customers_mapped = {str(k): float(v) for k, v in raw_top_custs.items()}
                
                # 5. Process 3-Tier Customer Value Plan (50% / 44% / 6%) Natively from File
                customer_spend = df.groupby(cust_c)[sales_c].sum().reset_index()
                customer_spend['Spend_Rank_Pct'] = customer_spend[sales_c].rank(pct=True, method='first')
                
                def assign_custom_tier(pct):
                    if pct <= 0.50:
                        return 'Low Value'
                    elif pct <= 0.94:
                        return 'Medium Value'
                    else:
                        return 'High Value'
                
                customer_spend['Tier_Rank'] = customer_spend['Spend_Rank_Pct'].apply(assign_custom_tier)
                
                tier_mapping = dict(zip(customer_spend[cust_c], customer_spend['Tier_Rank']))
                df['Customer Segment'] = df[cust_c].map(tier_mapping)
                
                # Compute unique consumer splits matching original criteria
                segment_counts = df.groupby('Customer Segment')[cust_c].nunique().to_dict()
                print(f"📊 DATA ENGINE: Successfully computed authentic custom segments: {segment_counts}")
                
                # 6. Product Categories Performance Matrix
                product_perf = df.groupby(cat_c)[sales_c].sum().sort_values(ascending=False).to_dict()
                
                # 7. Market profit series
                market_prof = df.groupby(market_c)[profit_c].sum().sort_values(ascending=False).to_dict()

                # --- STEP 8: PRODUCTION COMPREHENSIVE GLOBAL MAP REALIGNMENT ---
                geo_map_data = df.groupby(country_c).agg({sales_c: 'sum', profit_c: 'sum'}).reset_index()
                
                # Master Absolute Real-World Coordinate Dictionary covering the entire dataset footprint
                coordinate_cache = {
                    # North America
                    "United States": [37.0902, -95.7129], "Canada": [56.1304, -106.3468], "Mexico": [23.6345, -102.5528],
                    # Central America & Caribbean
                    "Cuba": [21.5218, -77.7812], "Dominican Republic": [18.7357, -70.1627], "El Salvador": [13.7942, -88.8965],
                    "Guatemala": [15.7835, -90.2308], "Honduras": [15.2000, -86.2419], "Nicaragua": [12.8654, -85.2072],
                    "Panama": [8.5380, -80.7821], "Haiti": [18.9712, -72.2852], "Jamaica": [18.1096, -77.2975],
                    "Trinidad and Tobago": [10.6918, -61.2225], "Barbados": [13.1939, -59.5432], "Guadeloupe": [16.2650, -61.5510],
                    "Martinique": [14.6415, -61.0242],
                    # South America
                    "Brazil": [-14.2350, -51.9253], "Argentina": [-38.4161, -63.6167], "Chile": [-35.6751, -71.5430],
                    "Colombia": [4.5709, -74.2973], "Peru": [-9.1900, -75.0152], "Venezuela": [6.4238, -66.5897],
                    "Bolivia": [-16.2902, -63.5887], "Paraguay": [-23.4425, -58.4438], "Uruguay": [-32.5228, -55.7658],
                    "Ecuador": [-1.8312, -78.1834],
                    # Europe
                    "United Kingdom": [55.3781, -3.4360], "France": [46.2276, 2.2137], "Germany": [51.1657, 10.4515],
                    "Italy": [41.8719, 12.5674], "Spain": [40.4637, -3.7492], "Netherlands": [52.1326, 5.2913],
                    "Sweden": [60.1282, 18.6435], "Austria": [47.5162, 14.5501], "Belgium": [50.5039, 4.4699],
                    "Denmark": [56.2639, 9.5018], "Finland": [61.9241, 25.7482], "Ireland": [53.4129, -8.2439],
                    "Norway": [60.4720, 8.4689], "Portugal": [39.3999, -8.2245], "Switzerland": [46.8182, 8.2275],
                    "Poland": [51.9194, 19.1451], "Russia": [61.5240, 105.3188], "Ukraine": [48.3794, 31.1656],
                    "Czech Republic": [49.8175, 15.4730], "Romania": [45.9432, 24.9668], "Hungary": [47.1625, 19.5033],
                    "Belarus": [53.7098, 27.9534], "Bulgaria": [42.7339, 25.4858], "Croatia": [45.1000, 15.2000],
                    "Slovakia": [48.6690, 19.6990], "Slovenia": [46.1512, 14.9955], "Bosnia and Herzegovina": [43.9159, 17.6791],
                    "Albania": [41.1533, 20.1683], "Macedonia": [41.6086, 21.7453], "Montenegro": [42.7087, 19.3744],
                    "Moldova": [47.4116, 28.3699], "Estonia": [58.5953, 25.0136], "Lithuania": [55.1694, 23.8813],
                    # Asia & Middle East
                    "China": [35.8617, 104.1954], "India": [20.5937, 78.9629], "Japan": [36.2048, 138.2529],
                    "Australia": [-25.2744, 133.7751], "New Zealand": [-40.9006, 174.8860], "Singapore": [1.3521, 103.8198],
                    "Indonesia": [-0.7893, 113.9213], "Philippines": [12.8797, 121.7740], "Thailand": [15.8700, 100.9925],
                    "Vietnam": [14.0583, 108.2772], "Malaysia": [4.2105, 101.9758], "Pakistan": [30.3753, 69.3451],
                    "Bangladesh": [23.6850, 90.3563], "Myanmar (Burma)": [21.9162, 95.9560], "Cambodia": [12.5657, 104.9910],
                    "Nepal": [28.3949, 84.1240], "Sri Lanka": [7.8731, 80.7718], "Taiwan": [23.6978, 120.9605],
                    "Hong Kong": [22.3193, 114.1694], "Turkey": [38.9637, 35.2433], "Saudi Arabia": [23.8859, 45.0792],
                    "Israel": [31.0461, 34.8516], "Iran": [32.4279, 53.6880], "Iraq": [33.2232, 43.6793],
                    "Jordan": [30.5852, 36.2384], "Lebanon": [33.8547, 35.8623], "Syria": [34.8021, 38.9968],
                    "Yemen": [15.5527, 48.5164], "United Arab Emirates": [23.4241, 53.8478], "Bahrain": [26.0667, 50.5577],
                    "Qatar": [25.3548, 51.1839], "Kazakhstan": [48.0196, 66.9237], "Uzbekistan": [41.3775, 64.5853],
                    "Azerbaijan": [40.1431, 47.5769], "Georgia": [42.3154, 43.3569], "Armenia": [40.0691, 45.0382],
                    "Kyrgyzstan": [41.2044, 74.7661], "Tajikistan": [38.8610, 71.2761], "Turkmenistan": [38.9697, 59.5563],
                    # Africa
                    "South Africa": [-30.5595, 22.9375], "Nigeria": [9.0820, 8.6753], "Egypt": [26.8206, 30.8025],
                    "Morocco": [31.7917, -7.0926], "Algeria": [28.0339, 1.6596], "Libya": [26.3351, 17.2283],
                    "Tunisia": [33.8869, 9.5375], "Sudan": [12.8628, 30.2176], "Kenya": [-0.0236, 37.9062],
                    "Ghana": [7.9465, -1.0232], "Cameroon": [7.3697, 12.3547], "Angola": [-11.2027, 17.8739],
                    "Tanzania": [-6.3690, 34.8888], "Uganda": [1.3733, 32.2903], "Zambia": [-13.1338, 27.8493],
                    "Zimbabwe": [-19.0154, 29.1549], "Mozambique": [-18.6657, 35.5296], "Madagascar": [-18.7669, 46.8691],
                    "Senegal": [14.4974, -14.4524], "Mali": [17.5707, -3.9962], "Ivory Coast": [7.5400, -5.5471],
                    "Cote d'Ivoire": [7.5400, -5.5471], "Democratic Republic of the Congo": [-4.0383, 21.7587],
                    "Republic of the Congo": [-0.2280, 15.8277], "Central African Republic": [6.6111, 20.9394],
                    "Chad": [15.4542, 18.7322], "Niger": [17.6078, 8.0817], "Benin": [9.3077, 2.3158],
                    "Togo": [8.6195, 0.8248], "Liberia": [6.4281, -9.4295], "Sierra Leone": [8.4606, -11.7799],
                    "Guinea": [9.9456, -9.6966], "Guinea-Bissau": [11.8037, -15.1804], "Gabon": [-0.8037, 11.6094],
                    "Equatorial Guinea": [1.6508, 10.2679], "Burundi": [-3.3731, 29.9189], "Rwanda": [-1.9403, 29.8739],
                    "Somalia": [5.1521, 46.1996], "Ethiopia": [9.1450, 40.4897], "Eritrea": [15.1794, 39.7823],
                    "Djibouti": [11.8251, 42.5903], "Namibia": [-22.9576, 18.4904], "Lesotho": [-29.6099, 28.2336],
                    "Swaziland": [-26.5225, 31.4659], "Mauritania": [21.0079, -10.9408],
                    "Afghanistan": [33.9391, 67.7100],
                    "Mongolia": [46.8625, 103.8467],
                    "Papua New Guinea": [-6.3150, 143.9555],
                    "South Korea": [35.9078, 127.7669],
                    "South Sudan": [6.8770, 31.3070],
                }

                geo_list = []
                for _, row in geo_map_data.iterrows():
                    country_name = str(row[country_c]).strip()
                    if not country_name or country_name.lower() == 'nan':
                        continue
                        
                    if country_name in coordinate_cache:
                        coords = coordinate_cache[country_name]
                        geo_list.append({
                            "country": country_name,
                            "sales": float(row[sales_c]),
                            "profit": float(row[profit_c]),
                            "lat": coords[0],
                            "lng": coords[1]
                        })
                    else:
                        print(f"⚠️ MAP CHECK: Country string unmapped: '{country_name}'")
                
                # Assemble complete live analytical payload
                payload = {
                    "kpis": {
                        "total_sales": round(total_sales, 2),
                        "total_orders": total_orders,
                        "aov": round(aov, 2),
                        "total_customers": total_customers
                    },
                    "segments": segment_counts,
                    "products": product_perf,
                    "markets": market_prof,
                    "real_top_products": top_products_mapped,
                    "real_top_customers": top_customers_mapped,
                    "geo_map": geo_list
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(payload).encode('utf-8'))
                return
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
                return

        return super().do_GET()

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, LiveDashboardHandler)
    print("🚀 Live Portfolio Data Engine active at http://localhost:8000/dashboard/web/index.html")
    httpd.serve_forever()