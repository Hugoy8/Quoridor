module.exports = {
    purge: {
      content: [
        './src/**/*.{html,ts}', './projects/**/*.{html,ts}'
      ],
    },
    darkMode: false,
    theme: {
      fontFamily: {
        sans: ['Roboto', 'sans-serif'],
      },
      extend: {
        animation: {
          wiggle: 'wiggle 2s ease-in-out infinite',
        },
        fontSize: {
          's': '8px',
        },
        colors: {
          primary900: '#003E6A',
          primary800: '#0F67A7',
          primary700: '#1081D3',
          primary600: '#2DA6FF',
          primary500: '#11C6FF',
          primary400: '#39DBFF',
          primary300: '#88E9FF',
          primary200: '#B7F2FF',
          primary100: '#F0FCFF',
  
          neutral900: '#102A43',
          neutral800: '#243B53',
          neutral700: '#334E68',
          neutral600: '#486581',
          neutral500: '#829AB1',
          neutral400: '#9FB3C8',
          neutral300: '#BCCCDC',
          neutral200: '#D9E2EC',
          neutral100: '#F0F4F8',
  
          backgroundColor : '#FCFDFD',
          panelColor : '#F3FAFC',
          textOverlay : '#B3B3B3',
  
          lightBlueBg : '#CCF4FF',
          darkBlueIcon : '#0F4970',
          lightYellowBg : '#FFF3C4',
          darkYellowIcon : '#DE911D',
          lightGreenBg : '#D0FFD4',
          darkGreenIcon : '#0F9D1A',
        },
      },
    },
    variants: {
      extend: {},
    },
    plugins: []
}