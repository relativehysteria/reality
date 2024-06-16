IMAGES = """
    query AdvertDetail(
        $id: ID!,
    ) {
        advert(id: $id) {
            publicImages {
                url(filter: RECORD_MAIN)
            }
        }
    }
"""

INITIAL = """
    query AdvertList(
        $locale: Locale!,
        $estateType: [EstateType],
        $offerType: [OfferType],
        $disposition: [Disposition],
        $regionOsmIds: [ID],
        $limit: Int = 0,
        $order: ResultOrder = TIMEORDER_DESC,
        $priceFrom: Int,
        $priceTo: Int,
        $surfaceFrom: Int,
        $surfaceTo: Int,
        $roommate: Boolean,
        $currency: Currency
    ) {
        listAdverts(
            offerType: $offerType
            estateType: $estateType
            disposition: $disposition
            limit: $limit
            regionOsmIds: $regionOsmIds
            order: $order
            priceFrom: $priceFrom
            priceTo: $priceTo
            surfaceFrom: $surfaceFrom
            surfaceTo: $surfaceTo
            roommate: $roommate
            currency: $currency
        ) {
            list {
                uri
                id
                disposition
                mainImageUrl: mainImage {
                    url(filter: RECORD_THUMB)
                }
                address(locale: $locale)
                surface
                tags(locale: $locale)
                price
                charges
                reserved
                gps {
                    lat
                    lng
                }
            }
        }
        actionList: listAdverts(
            offerType: $offerType
            estateType: $estateType
            disposition: $disposition
            regionOsmIds: $regionOsmIds
            order: $order
            priceFrom: $priceFrom
            priceTo: $priceTo
            surfaceFrom: $surfaceFrom
            surfaceTo: $surfaceTo
            roommate: $roommate
        ) {
            totalCount
        }
    }
"""
