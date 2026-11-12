import serpapi
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from numpy.ma.core import min_val


# streamlit run app.py

def compare(medicine_name):
    api_key = st.secrets.get("SERPAPI_KEY")
    client = serpapi.Client(api_key=api_key)
    results = client.search({
        "engine": "google_shopping",
        "q": medicine_name
    })
    shopping_results = results.get("shopping_results", [])
    return shopping_results


col1, col2 = st.columns([1, 4], vertical_alignment="center")

with col1:
    st.image("e_pharmacy.png", width=200)

with col2:
    st.header("E-Pharmacy Price Comparison System")

# Details of Sidebar
st.sidebar.title("Enter Name of Medicine")
medicine_name = st.sidebar.text_input("Enter Name Here 👇🏽")
#number = st.sidebar.text_input("Enter Number of Options Here: 👇🏽", min_value=1, max_value=20, value=2, step=1)
number = st.sidebar.number_input(
    "Enter Number of Options Here: 👇🏽",
    min_value=1,
    max_value=20,
    value=2,
    step=1
)
medicine_company = []
medicine_price = []

if medicine_name:
    if st.sidebar.button("Show Price Comparison"):
        shopping_results = compare(medicine_name)

        if not shopping_results:
            st.warning("No results found.")
        else:
            lowest_price = None
            lowest_price_index = 0
            limit = min(int(number), len(shopping_results))

            for i in range(limit):
                item = shopping_results[i]
                raw_price = item.get('price')
                #-------------------------------------------------------------------
                # detailed fetched to plot a Bar graph
                medicine_company.append(item.get('source'))
                medicine_price.append(float(raw_price.replace('$', '').replace(',', '').strip()))

                #raw_price = str(item.get('price', 0)) # Alternate of above code
                #clean_price = raw_price.replace('$', '').replace(',', '').strip() # Alternate of above code
                #medicine_price.append(float(clean_price)) # Alternate of above code
                #--------------------------------------------------------------

                # Safely parse price string (removes '$' and commas)
                current_price = None
                if raw_price:
                    try:
                        current_price = float(raw_price.replace('$', '').replace(',', '').strip())
                    except ValueError:
                        pass

                st.title(f"Option {i + 1}")

                col1, col2 = st.columns(2)
                col1.write("Company Name:")
                col2.write(item.get('source', 'N/A'))

                col1.write("Medicine Name:")
                col2.write(item.get('title', 'N/A'))

                col1.write("Price:")
                col2.write(raw_price or 'N/A')

                col1.write("Old Price:")
                col2.write(item.get('old_price', 'N/A'))

                col1.write("Delivery Option:")
                col2.write(item.get('delivery', 'N/A'))

                url = item.get('product_link')
                col1.write("Link to Buy From")

                if url:
                    col2.write(f"[Link]({url})")

                else:
                    col2.write("No link available")

                thumb = item.get('thumbnail')
                col1.write("Thumbnail Link for Reference:")

                if thumb:
                    col2.write(f"[Link]({thumb})")

                else:
                    col2.write("No thumblink available")
                '''---------------------------------------------------------------'''

                # Update lowest price and index
                if current_price is not None:
                    if lowest_price is None or current_price < lowest_price:
                        lowest_price = current_price
                        lowest_price_index = i

        # Coding to propose best options:
        st.title("Best Options:")

        col1, col2 = st.columns(2)
        col1.write("Company Name:")
        col2.write(shopping_results[lowest_price_index].get('source'))

        col1.write("Medician Name:")
        col2.write(shopping_results[lowest_price_index].get('title'))

        col1.write("Price:")
        col2.write(shopping_results[lowest_price_index].get('price'))

        col1.write("Old Price:")
        col2.write(shopping_results[lowest_price_index].get('old_price'))

        col1.write("Delivery Option:")
        col2.write(shopping_results[lowest_price_index].get('delivery'))

        url = shopping_results[lowest_price_index].get('product_link')
        col1.write("Link to Buy From")
        col2.write(f"[Link]({url})")

        thumb = shopping_results[lowest_price_index].get('thumbnail')
        col1.write("Thumbnail Link for Reference")
        col2.write(f"[Link]({thumb})")

        st.sidebar.write("Best Price Product Picture")
        st.sidebar.image(shopping_results[lowest_price_index].get('thumbnail'),width=200)

        # -------- Price comparison showing in a form of Plot a Graph --------------------
        df = pd.DataFrame(medicine_price, medicine_company)
        st.title("Price Comparison in Bar Graph")
        st.bar_chart(df)

        # -------- Price comparison showing in a form of Pie Chart --------------------
        fig, ax = plt.subplots()
        ax.pie(medicine_price, labels=medicine_company, shadow=True)
        ax.axis('equal')
        st.pyplot(fig)









