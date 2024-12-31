{ pkgs ? import <nixpkgs> {} }:
let
  name = "rmlib";
  fhs = pkgs.buildFHSUserEnv({
    inherit name;
    targetPkgs = pkgs: [
      pkgs.util-linux
      pkgs.micromamba
      pkgs.tectonic
    ];
    profile = ''
      set -e
      export MAMBA_ROOT_PREFIX=${builtins.getEnv "PWD"}/.mamba
      eval "$(micromamba shell hook --shell=posix)"
      micromamba create --quiet --yes --override-channels --name ${name} --file conda-lock.yml
      micromamba run -n ${name} poetry install
      micromamba activate ${name}
      set +e
    '';
  });
in fhs.env
