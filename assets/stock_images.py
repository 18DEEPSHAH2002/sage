import streamlit as st

# Store URLs of stock images
stock_images = {
    'chart': [
        "https://pixabay.com/get/gfadf06733bd54c05fbb160c7dd3890d5eff3393c67086f45e6dbeb812b7e89e71d7904665ec31de116ace6baad35bd897c41b8daa5fdb827c9e870951ca74546_1280.jpg",
        "https://pixabay.com/get/g43142a76c26beea3ece4fb1691f6018026188f1e9781b6a740f4d19614ac251dcb69f15276e030a32d4df328f09b76863a7d3e7d8e1096c3f35fa37c18020d4a_1280.jpg",
        "https://pixabay.com/get/g0ab43e80a1faf2ef6080c7082001973fa627eefc38b12b2cba46d2c12aba7209537fb542259745bb71ed324c2994c5d778cb0414b034233ca3c5d6716e839b7b_1280.jpg",
        "https://pixabay.com/get/g245a7eae3620d3eafb53950f5192c87eac3530d45a9e0c069295d8bd8fec1721f8749eb8cabcaa218753e2a3200dcf30d6e1b01cadff59aa9f34a4b865d5c55b_1280.jpg",
        "https://pixabay.com/get/gbd4a23d9dbe16a1c7d4b950d43b2e0d11493b17bea4daee5fb7b49d3495e1682afb55993b280a57672ec5ea031537bcc8ee979903d889a1443d452afd4886bb4_1280.jpg",
        "https://pixabay.com/get/ga174dcae66051bb4e9a0821bf6fdc0d0f16d9ac2d7f612eba75cabc6c0879b343966aae582fbcd42113c5d14d15757ebbd78dc616d6d5ee5d7e313f9f64e8d16_1280.jpg"
    ],
    'dashboard': [
        "https://pixabay.com/get/ga5801f575af2a3fe3d3634401f342f371b3027044276dd123d99a08be347ffece1e7e87505a6f76a943555e602d9b125b76e9a00a660e1c4db8e7a3d9066b975_1280.jpg",
        "https://pixabay.com/get/g74b636ef1143022fef4e87e7c606dfffbd4d5038c83821ac150a5d97dfc9cc0ec4146e22f9d608b9b8fd8dbf0bbb4e58318202d177b655ac1a7aa36a9b954ec4_1280.jpg",
        "https://pixabay.com/get/g9e60f3884524643f893e53991693bb34d6de72ec733811cea9716ca10044e192acf0e7faa29d939c078e3c7c019b902f1d61a5677484e8ae38ce856d49c3b2b2_1280.jpg",
        "https://pixabay.com/get/g2d4f819f59c37773de3c70654146cacf104a0ba314d7728ebd44a5e62fb71ae6998236725e8505c46d7f99c862150830e8b40413589ff47340f2a86bccd0e928_1280.jpg"
    ],
    'business': [
        "https://pixabay.com/get/gd3ec3c92e163f5dd1771bcf79822ca1d6221e0ec9a9a6cd27a791d0192b0de31926bdd5f1b228e14524d8a4cfed89591b372535b6581faac41de980e5dc02148_1280.jpg",
        "https://pixabay.com/get/ge430a501925309db8816772046bb7fe1ca89dcb8f5a24bde6d5ce656e0c6f8576221889f9221a3a9e2737f9450d3a716a09b7e73d4df28ea50640662adbd07b4_1280.jpg"
    ]
}

def get_stock_image_url(category, index=None):
    """
    Get a stock image URL based on category and index
    
    Args:
        category (str): Image category ('chart', 'dashboard', or 'business')
        index (int, optional): Specific index to retrieve. If None, returns the first image.
    
    Returns:
        str: URL of the stock image
    """
    if category not in stock_images:
        # Default to 'chart' if category not found
        category = 'chart'
    
    images = stock_images[category]
    
    if index is None or index < 0 or index >= len(images):
        # Return first image if index is out of range
        return images[0]
    
    return images[index]
