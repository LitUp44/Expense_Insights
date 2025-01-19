import streamlit as st
import pandas as pd
import plotly.express as px

# Function to categorize ratios for each category
def categorize(value, category):
    if category == "Needs":
        if value < 60:
            return "low", "green"
        elif value <= 75:
            return "medium", "yellow"
        else:
            return "high", "red"
    elif category == "Savings":
        if value > 20:
            return "high", "green"
        elif value < 15:
            return "low", "red"
        elif value <= 20:
            return "medium", "yellow"
    elif category == "Wants":
        if value < 10:
            return "low", "green"
        elif value <= 20:
            return "medium", "yellow"
        else:
            return "high", "red"

# Function to determine the color of Wants based on Savings
def wants_color_func(savings_cat, wants_percentage):
    if savings_cat == "low" and wants_percentage > 20:
        return "red"
    else:
        return "green"

# Function to determine insights based on categories
def get_insight(savings_cat, wants_cat, needs_cat):
    if savings_cat == "low" and wants_cat == "low" and needs_cat == "low":
        return "Not possible"
    elif savings_cat == "low" and wants_cat == "low" and needs_cat == "medium":
        return "Your needs are on the high side, this can cause stress by not leaving quite enough money for your savings or wants. Try getting your needs to 60% to free up some extra money to be able to enjoy now and in the future"
    elif savings_cat == "low" and wants_cat == "low" and needs_cat == "high":
        return "Your needs are much higher than the recommended 60%. This is frequently a source of anxiety as it can feel like the money is flying out as fast as it comes in. Reviewing your priorities and reducing the money you HAVE to spend every month is a priority."
    elif savings_cat == "low" and wants_cat == "medium" and needs_cat == "low":
        return "Not possible"
    elif savings_cat == "low" and wants_cat == "medium" and needs_cat == "medium":
        return "Your needs are on the high side, this can cause stress by not leaving quite enough money for your savings. Try getting your needs to 60% to free up some extra money to be able to enjoy in the future"
    elif savings_cat == "low" and wants_cat == "medium" and needs_cat == "high":
        return "Your needs are much higher than the recommended 60%. This is frequently a source of anxiety as it can feel like the money is flying out as fast as it comes in. Reviewing your priorities and reducing the money you HAVE to spend every month is a priority."
    elif savings_cat == "low" and wants_cat == "high" and needs_cat == "low":
        return "Your needs are below the recommended 60% which is great, but by allocating more than 20% to wants you aren't leaving quite enough for your savings. Re-allocating your wants even slightly will make a huge difference to your long-term future."
    elif savings_cat == "low" and wants_cat == "high" and needs_cat == "medium":
        return "Your needs and wants are both higher than recommended - reducing these to be able to reallocate to your savings will go a long way in setting you up for future success"
    elif savings_cat == "low" and wants_cat == "high" and needs_cat == "high":
        return "Your needs and wants are both much higher than recommended - this may be causing anxiety as it feels like money is leaving faster than it's coming in. Reducing these to be able to reallocate to your savings will go a long way in setting you up for future success."
    elif savings_cat == "medium" and wants_cat == "low" and needs_cat == "low":
        return "Not possible"
    elif savings_cat == "medium" and wants_cat == "low" and needs_cat == "medium":
        return "Your needs are on the high side, this can cause stress by not leaving quite enough money for your savings or wants. Try getting your needs to 60% to free up some extra money to be able to enjoy now and in the future"
    elif savings_cat == "medium" and wants_cat == "low" and needs_cat == "high":
        return "Your needs are much higher than the recommended 60%. This means you have very little to allocate to wants - the things that make life exciting and fun. Reallocating some money where possible from your needs may go a long way to helping you live a more fulfilling life."
    elif savings_cat == "medium" and wants_cat == "medium" and needs_cat == "low":
        return "Not possible"
    elif savings_cat == "medium" and wants_cat == "medium" and needs_cat == "medium":
        return "Your numbers are looking pretty good! A little bit higher than recommended on your needs but very close so if you feel happy with your progress towards savings and you're happy with the money you have for fun in your life then no need to make changes."
    elif savings_cat == "medium" and wants_cat == "medium" and needs_cat == "high":
        return "Not possible"
    elif savings_cat == "medium" and wants_cat == "high" and needs_cat == "low":
        return "You have a great handle on your finances. If you want a small suggestion, getting your savings up to 20% will set you on a great course for the long-term."
    elif savings_cat == "medium" and wants_cat == "high" and needs_cat == "medium":
        return "Your needs and your wants are both a little on the high side meaning you're not quite hitting our recommended savings goal of 20%. Adjusting your wants a little bit will go a long way for your future!"
    elif savings_cat == "medium" and wants_cat == "high" and needs_cat == "high":
        return "Not possible"
    elif savings_cat == "high" and wants_cat == "low" and needs_cat == "low":
        return "Wow - those are some amazing numbers, you are above your savings and below your wants and needs. This is a great place to think about whether you want to spend MORE on enriching your life!"
    elif savings_cat == "high" and wants_cat == "low" and needs_cat == "medium":
        return "You're doing great, savings are super healthy but needs are a little higher compared to wants. If it's possible, have a look at whether you want to adjust some of your needs to be able to allocate more to your short term wants!"
    elif savings_cat == "high" and wants_cat == "low" and needs_cat == "high":
        return "Your wants are very low compared to your savings and needs. Getting your needs closer to the recommended 60% may go a long way in helping you feel you have freedom and flexibility with your money."
    elif savings_cat == "high" and wants_cat == "medium" and needs_cat == "low":
        return "Wow - these are some great numbers! You may want to even think about whether you want to spend even MORE on your wants to enrich your life."
    elif savings_cat == "high" and wants_cat == "medium" and needs_cat == "medium":
        return "These are some great numbers - if you wanted any ideas, adjusting your needs percentage to be slightly closer to the target 60% will free up more money to put to your wants, helping you feel freedom and fun with your money."
    elif savings_cat == "high" and wants_cat == "medium" and needs_cat == "high":
        return "not possible"
    elif savings_cat == "high" and wants_cat == "high" and needs_cat == "low":
        return "These are some great numbers, lots going to both your savings and wants. No notes."
    elif savings_cat == "high" and wants_cat == "high" and needs_cat == "medium":
        return "not possible"
    elif savings_cat == "high" and wants_cat == "high" and needs_cat == "high":
        return "not possible"
    else:
        return "No specific insight available for this combination."

# Streamlit app layout

st.image("alignedLogo.png", use_container_width=False, width=700)


st.title("Financial Fitness Calculator")

# Explanatory text with a background color
st.markdown("""
<div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 20px;">

Let's help you understand your budget breakdown! Simply input your average monthly numbers across your **Savings**, **Wants**, and **Needs**.

Assume that your income gets spent three ways. Your **Needs** which is everything you **have** to spend per month. Your rent, utilities, groceries, subsciptions, pre-paid classes, etc.

Your **wants** is anything you spend on variable purchases; going out, movies, travel, etc.

Finally **saving** - how much on average goes to saving or investing of any kind. Don't worry too much if you have pre-tax money going to retirement accounts, just pick a rough number.
</div>
""", unsafe_allow_html=True)

# User input for savings, wants, and needs amounts (totals)
savings_total = st.number_input("Total Savings", min_value=0, step=100, value=1000)
wants_total = st.number_input("Total Wants", min_value=0, step=100, value=1000)
needs_total = st.number_input("Total Needs", min_value=0, step=100, value=3000)

# Calculate the total income based on the inputs
total_income = savings_total + wants_total + needs_total

# Calculate the percentages of total income
savings_percentage = (savings_total / total_income) * 100
wants_percentage = (wants_total / total_income) * 100
needs_percentage = (needs_total / total_income) * 100

# Categorize each value and assign color
savings_cat, savings_color = categorize(savings_percentage, "Savings")
wants_cat, wants_color = categorize(wants_percentage, "Wants")
needs_cat, needs_color = categorize(needs_percentage, "Needs")

# Adjust the wants color based on savings
wants_color = wants_color_func(savings_cat, wants_percentage)

# Prepare data for visualization
data = pd.DataFrame({
    'Category': ['Savings', 'Wants', 'Needs'],
    'Amount': [savings_total, wants_total, needs_total],
    'Percentage': [savings_percentage, wants_percentage, needs_percentage],
    'Color': [savings_color, wants_color, needs_color]
})

# Create pie chart
fig = px.pie(data, names='Category', values='Amount', color='Color',
             title="Budget Allocation", color_discrete_map={
                 'green': 'green',
                 'yellow': 'yellow',
                 'red': 'red'
             })
fig.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1],
                  marker=dict(line=dict(color='black', width=2)))
fig.update_layout(margin=dict(t=50, b=50, l=50, r=50),
                  plot_bgcolor='#f7f7f7', paper_bgcolor='#ffffff',
                  font=dict(family="Arial", size=14, color="black"))

# Separator above results
st.markdown("---")

# Display formatted results
st.markdown("### Results")
st.markdown(f"**Savings:** **{savings_percentage:.2f}%**")
st.markdown(f"**Wants:** **{wants_percentage:.2f}%**")
st.markdown(f"**Needs:** **{needs_percentage:.2f}%**")

# Get and display insights
insight = get_insight(savings_cat, wants_cat, needs_cat)
st.markdown(f"""
<div style="background-color: #f1f1f1; border-radius: 10px; padding: 10px; margin-top: 10px; font-size: 16px; font-weight: bold;">
📢 Insight: {insight}
</div>
""", unsafe_allow_html=True)

# Display the pie chart
st.plotly_chart(fig)

