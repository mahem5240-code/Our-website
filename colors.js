// Central palette map so every card/badge/indicator uses consistent,
// accessible color pairs in both light and dark mode.
export const COLOR_MAP = {
  blue: {
    dot: 'bg-[#0071E3]',
    text: 'text-[#0071E3]',
    bg: 'bg-[#0071E3]/8 dark:bg-[#0071E3]/15',
    ring: 'ring-[#0071E3]/25',
    grad: 'from-[#0071E3] to-[#42A5F5]',
  },
  indigo: {
    dot: 'bg-[#5E5CE6]',
    text: 'text-[#5E5CE6]',
    bg: 'bg-[#5E5CE6]/8 dark:bg-[#5E5CE6]/15',
    ring: 'ring-[#5E5CE6]/25',
    grad: 'from-[#5E5CE6] to-[#8E8CF0]',
  },
  teal: {
    dot: 'bg-[#0AB8B0]',
    text: 'text-[#0AB8B0]',
    bg: 'bg-[#0AB8B0]/8 dark:bg-[#0AB8B0]/15',
    ring: 'ring-[#0AB8B0]/25',
    grad: 'from-[#0AB8B0] to-[#57D8CF]',
  },
  orange: {
    dot: 'bg-[#FF9F0A]',
    text: 'text-[#FF9F0A]',
    bg: 'bg-[#FF9F0A]/8 dark:bg-[#FF9F0A]/15',
    ring: 'ring-[#FF9F0A]/25',
    grad: 'from-[#FF9F0A] to-[#FFC24D]',
  },
  pink: {
    dot: 'bg-[#FF375F]',
    text: 'text-[#FF375F]',
    bg: 'bg-[#FF375F]/8 dark:bg-[#FF375F]/15',
    ring: 'ring-[#FF375F]/25',
    grad: 'from-[#FF375F] to-[#FF7A93]',
  },
  green: {
    dot: 'bg-[#30D158]',
    text: 'text-[#30D158]',
    bg: 'bg-[#30D158]/8 dark:bg-[#30D158]/15',
    ring: 'ring-[#30D158]/25',
    grad: 'from-[#30D158] to-[#6EE38B]',
  },
  purple: {
    dot: 'bg-[#BF5AF2]',
    text: 'text-[#BF5AF2]',
    bg: 'bg-[#BF5AF2]/8 dark:bg-[#BF5AF2]/15',
    ring: 'ring-[#BF5AF2]/25',
    grad: 'from-[#BF5AF2] to-[#D68CFA]',
  },
}

export const colorFor = (key) => COLOR_MAP[key] || COLOR_MAP.blue
