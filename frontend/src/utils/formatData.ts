export function formatNumber(
  value: string | number | null,
  decimals = 2,
  trimZeros = true
): string {
  if (value === null || value === undefined) return "-"
  const num = Number(value)
  if (isNaN(num)) return String(value)

  let formatted = num.toFixed(decimals)
  return trimZeros ? formatted.replace(/\.?0+$/, "") : formatted
}
