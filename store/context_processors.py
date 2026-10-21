
def category_menus(request):
    menu_data = {
        'Women': [
            ('Footwear', 'Explore everyday shoes and sandals.'),
            ('Sneakers', 'Casual sneakers for daily wear.'),
            ('Heels', 'Elegant styles for every occasion.'),
            ('Flats', 'Comfortable styles for daily use.'),
            ('Sandals', 'Easy-to-wear open footwear.'),
            ('Sports Shoes', 'Shoes for active lifestyles.'),
            ('New Arrivals', 'Discover the latest collections.'),
            ('Best Sellers', 'Shop popular customer favourites.'),
        ],
        'Men': [
            ('Casual Shoes', 'Everyday styles for every outfit.'),
            ('Sneakers', 'Modern sneakers for daily comfort.'),
            ('Formal Shoes', 'Smart styles for work and events.'),
            ('Sports Shoes', 'Supportive footwear for activity.'),
            ('Sandals', 'Comfortable footwear for casual days.'),
            ('Slippers', 'Easy footwear for everyday use.'),
            ('New Arrivals', 'Explore the latest styles.'),
            ('Best Sellers', 'Discover popular choices.'),
        ],
        'Kids': [
            ('Boys', 'Fun footwear for growing feet.'),
            ('Girls', 'Colourful styles for every day.'),
            ('School Shoes', 'Everyday school-ready footwear.'),
            ('Sports Shoes', 'Active styles for playtime.'),
            ('Sneakers', 'Cool looks for young trendsetters.'),
            ('Sandals', 'Comfortable options for outings.'),
            ('New Arrivals', 'See the newest kids collection.'),
            ('Best Sellers', 'Popular picks for little feet.'),
        ],
        'Brands': [
            ('All Brands', 'Explore the full brand collection.'),
            ('Premium', 'Discover premium footwear styles.'),
            ('Sportswear', 'Find footwear for active days.'),
            ('Casual', 'Relaxed styles for everyday wear.'),
            ('Formal', 'Footwear for work and occasions.'),
            ('Trending', 'Explore popular brand styles.'),
            ('New Brands', 'Discover something new.'),
            ('Top Picks', 'Browse our recommended styles.'),
        ],
        'Offers': [
            ('All Offers', 'Explore current special offers.'),
            ('Under ₹499', 'Shop styles at lower prices.'),
            ('Under ₹999', 'Find more styles within budget.'),
            ('Women’s Deals', 'Offers on women’s footwear.'),
            ('Men’s Deals', 'Offers on men’s footwear.'),
            ('Kids’ Deals', 'Save on kids’ footwear.'),
            ('Clearance', 'Explore selected reduced-price styles.'),
            ('Best Deals', 'Discover our featured offers.'),
        ],
    }

    categories = []
    for name, entries in menu_data.items():
        categories.append({
            'name': name,
            'url': f"/#{name.lower()}",
            'items': [
                {'heading': heading, 'description': description}
                for heading, description in entries
            ],
        })

    return {'categories': categories}
