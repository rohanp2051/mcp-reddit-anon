{
  description = "MCP Reddit Server (Anonymous, no credentials required)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python313;

        pythonEnv = python.withPackages (ps: [
          ps.fastmcp
          ps.uvicorn
        ]);

        mcp-reddit-anon = python.pkgs.buildPythonApplication {
          pname = "mcp-reddit-anon";
          version = "0.1.0";
          pyproject = true;

          src = ./.;

          build-system = [ python.pkgs.hatchling ];

          dependencies = with python.pkgs; [
            fastmcp
            uvicorn
          ];

          meta = {
            description = "MCP server for fetching Reddit content anonymously";
            homepage = "https://github.com/rohanp2051/mcp-reddit-anon";
            license = pkgs.lib.licenses.mit;
          };
        };
      in
      {
        packages = {
          default = mcp-reddit-anon;
          mcp-reddit-anon = mcp-reddit-anon;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
          ];

          shellHook = ''
            export PYTHONPATH="$PWD/src:$PYTHONPATH"
          '';
        };
      }
    );
}
