export function productImageClass(url: string): string {
  const isPhoto = /\.(avif|webp|png|jpe?g|gif)(\?|$)/i.test(url);
  return isPhoto
    ? "product-thumb product-thumb--photo"
    : "product-thumb product-thumb--illustration";
}

export function ProductImage({
  src,
  className,
}: {
  src: string;
  className?: string;
}) {
  const base = productImageClass(src);
  return (
    <img
      src={src}
      alt=""
      className={className ? `${base} ${className}` : base}
      loading="lazy"
    />
  );
}
