import assert from 'node:assert/strict';
import { resolve } from 'node:path';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const client = new Client({ name: 'posterly-plugin-runtime-test', version: '1.0.0' });
await client.connect(new StdioClientTransport({
  command: process.execPath,
  args: [resolve('node_modules/posterly-mcp-server/dist/index.js')],
  env: { PATH: process.env.PATH, POSTERLY_DIRECTORY_PROFILE: 'claude', POSTERLY_API_KEY: 'test', POSTERLY_API_URL: 'http://127.0.0.1:1/api/v1' },
}));
try {
  const { tools } = await client.listTools();
  assert.equal(tools.length, 55);
  for (const name of ['generate_image', 'generate_video', 'list_jobs', 'resume_subscription', 'cancel_subscription', 'get_image_job', 'update_post_status']) {
    assert(!tools.some(tool => tool.name === name), name);
    const result = await client.callTool({ name, arguments: {} });
    assert.equal(result.isError, true, name);
    assert.match(result.content.map(item => item.text ?? '').join('\n'), /not found|unknown tool/i, name);
  }
  console.log('Published Claude plugin runtime passed: 55 tools; excluded tools and legacy aliases are unavailable.');
} finally { await client.close(); }
