# Links every skill in this repo into Claude Code and Codex, and sets up your
# private personal folder. Run again any time; `git pull` then updates all projects.
#   .\install.ps1          link with junctions (recommended, no admin needed)
#   .\install.ps1 -Copy    copy instead of link
param([switch]$Copy)
$ErrorActionPreference = "Stop"

$Repo = $PSScriptRoot
$Targets = @("$HOME\.claude\skills", "$HOME\.codex\skills")
$Personal = "$HOME\.ai-skills\personal"

foreach ($target in $Targets) {
  New-Item -ItemType Directory -Force -Path $target | Out-Null
  Get-ChildItem -Directory "$Repo\skills" | Where-Object { $_.Name -ne "_template" } | ForEach-Object {
    $dest = Join-Path $target $_.Name
    $existing = Get-Item $dest -ErrorAction SilentlyContinue
    if ($existing -and -not $existing.LinkType) {
      Write-Host "skip  $dest (a real folder is already there; move it to install this one)"
      return
    }
    if ($existing) { $existing.Delete() }
    if ($Copy) { Copy-Item -Recurse $_.FullName $dest }
    else { New-Item -ItemType Junction -Path $dest -Target $_.FullName | Out-Null }
    Write-Host "ok    $dest"
  }
}

if (-not (Test-Path "$Personal\taste.md")) {
  New-Item -ItemType Directory -Force -Path "$Personal\styles" | Out-Null
  Copy-Item "$Repo\skills\design-kit\personal-template\taste.md" "$Personal\taste.md"
  Write-Host "made  $Personal\taste.md (private, edit it to set your taste)"
} else {
  Write-Host "keep  $Personal\taste.md (already set up)"
}
