            else:  # If there is no high bid we only have to check the starting bid

        # Finally, if we passed at least one of the checks up there, we can return true
        messages.add_message(
            request, messages.SUCCESS, 'Added your bid. You are currently the high bidder.')

        return redirect('listing', id)


                      <div class="mb-3">
                            <!-- <label for="bid" class="form-label">Bid Amount in US Dollars:</label> -->
                            <input type="text" name="bid_amount:" id="bid"
                                placeholder='{{listing.starting_bid|floatformat:2|intcomma}}' class="form-control">
                        </div>