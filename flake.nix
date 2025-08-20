{
  description = "metatron exporter venv";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      nixpkgs,
      uv2nix,
      pyproject-nix,
      pyproject-build-systems,
      ...
    }:
    let
      inherit (nixpkgs) lib;

      systems = [
        "aarch64-darwin"
        "x86_64-linux"
      ];

      systemAttrs = f: system: { ${system} = f system; };

      mapSystems = f: systems |> lib.map (systemAttrs f) |> lib.mergeAttrsList;

      workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };

      overlay = workspace.mkPyprojectOverlay {
        sourcePreference = "wheel";
      };

      pyprojectOverrides = _final: _prev: { };

      pkgs = mapSystems (
        system:
        import nixpkgs {
          inherit system;
        }
      );

      python = mapSystems (system: pkgs.${system}.python311);

      pythonSet = mapSystems (
        system:
        (pkgs.${system}.callPackage pyproject-nix.build.packages {
          python = python.${system};
        }).overrideScope
          (
            lib.composeManyExtensions [
              pyproject-build-systems.overlays.default
              overlay
              pyprojectOverrides
            ]
          )
      );

      virtualenv = mapSystems (
        system: pythonSet.${system}.mkVirtualEnv "metatron-exporter-venv" workspace.deps.default
      );

    in
    {
      packages = mapSystems (system: {
        default = virtualenv.${system};
      });

      devShells = mapSystems (system: {
        impure = pkgs.${system}.mkShell {
          packages = [
            python.${system}
            pkgs.${system}.uv
          ];
          env = {
            UV_PYTHON_DOWNLOADS = "never";
            UV_PYTHON = python.${system}.interpreter;
          }
          // lib.optionalAttrs pkgs.${system}.stdenv.isLinux {
            LD_LIBRARY_PATH = lib.makeLibraryPath pkgs.${system}.pythonManylinuxPackages.manylinux1;
          };
          shellHook = ''
            unset PYTHONPATH
          '';
        };

        default = pkgs.${system}.mkShell {
          packages = [
            virtualenv.${system}
            pkgs.${system}.uv
          ];

          env = {
            UV_NO_SYNC = "1";
            UV_PYTHON = python.${system}.interpreter;
            UV_PYTHON_DOWNLOADS = "never";
          };

          shellHook = ''
            unset PYTHONPATH
            export REPO_ROOT=$(git rev-parse --show-toplevel)
          '';
        };
      });
    };
}
