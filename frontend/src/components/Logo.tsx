export interface LogoProps extends React.ComponentPropsWithoutRef<"svg"> {
  size?: number | string;
}

export function Logo({ size, ...others }: LogoProps) {
  return (
    <h1>Code search with AI</h1>
  );
}
