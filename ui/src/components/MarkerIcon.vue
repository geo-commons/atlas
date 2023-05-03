<template>
  <svg width="34px" height="42px" viewBox="0 0 34 42">
    <defs>
      <path
        id="path-1"
        d="M14,0 C6.07405021,0 0,6.15831449 0,14.4 C0,19.8887032 4.32900835,26.5537425 12.6510291,34.1565763 L14,35.3889694 L15.3489709,34.1565763 C23.6709917,26.5537425 28,19.8887032 28,14.4 C28,6.15831449 21.9259498,0 14,0 Z"
      ></path>
      <filter
        id="filter-2"
        x="-16.1%"
        y="-12.7%"
        width="132.1%"
        height="125.4%"
        filterUnits="objectBoundingBox"
      >
        <feOffset
          dx="0"
          dy="0"
          in="SourceAlpha"
          result="shadowOffsetOuter1"
        ></feOffset>
        <feGaussianBlur
          stdDeviation="1.5"
          in="shadowOffsetOuter1"
          result="shadowBlurOuter1"
        ></feGaussianBlur>
        <feColorMatrix
          values="0 0 0 0 0   0 0 0 0 0   0 0 0 0 0  0 0 0 0.25 0"
          type="matrix"
          in="shadowBlurOuter1"
        ></feColorMatrix>
      </filter>
    </defs>
    <g id="Group" transform="translate(3.000000, 3.000000)" fill-rule="nonzero">
      <use
        fill="black"
        fill-opacity="1"
        filter="url(#filter-2)"
        xlink:href="#path-1"
      ></use>
      <use :fill="strokeColor" xlink:href="#path-1"></use>
      <path
        :fill="fillColor"
        d="M14,2 C20.7,2 26,7.14 26,14.4 C26,19.08 22.1,25.28 14,32.68 C5.9,25.28 2,19.08 2,14.4 C2,7.14 7.3,2 14,2 Z M14,10 C11.8,10 10,11.8 10,14 C10,16.2 11.8,18 14,18 C16.2,18 18,16.2 18,14 C18,11.8 16.2,10 14,10 Z"
      ></path>
    </g>
  </svg>
</template>

<script>
export default {
  props: ["fillColor", "strokeColor"],
};
</script>
