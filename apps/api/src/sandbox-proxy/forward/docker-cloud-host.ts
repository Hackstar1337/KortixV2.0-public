export const DOCKER_CLOUD_FORWARDED_HOST_HEADER = 'x-kortix-docker-cloud-forwarded-host';

/** Docker's public port edge rejects client-supplied X-Forwarded-Host. */
export function remapDockerCloudHost(headers: Headers, provider: string): void {
  if (provider !== 'docker-cloud') return;
  const host = headers.get('x-forwarded-host');
  headers.delete(DOCKER_CLOUD_FORWARDED_HOST_HEADER);
  if (host) headers.set(DOCKER_CLOUD_FORWARDED_HOST_HEADER, host);
  headers.delete('x-forwarded-host');
}
