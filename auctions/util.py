def check_bid(bid, list):
    """
    Check if the given offer is bigger than start price and previous offers
    return True or False
    """
    if bid >= float(list.start_bid) and (list.start_bid is None or bid > float(list.current_bid)):
        return True
    return False
