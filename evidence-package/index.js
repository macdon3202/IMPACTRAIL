export const IMPACT_RAIL_RELEASE = Object.freeze({
  project: 'ImpactRail',
  version: '1.0.0',
  purpose: 'canonical public-goods impact verification fixture',
  sources: Object.freeze(['github-api', 'npm-registry', 'snapshot-hub']),
});

export function verifyFixtureShape(value) {
  return Boolean(value && value.project === IMPACT_RAIL_RELEASE.project && value.version === IMPACT_RAIL_RELEASE.version);
}
