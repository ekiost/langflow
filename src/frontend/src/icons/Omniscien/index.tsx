import React, { forwardRef } from "react";
import Omniscien from "./Omniscien";

export const OmniscienIcon = forwardRef<
    SVGSVGElement,
    React.PropsWithChildren<{}>
>((props, ref) => {
    return <Omniscien ref={ref} {...props} />;
});
