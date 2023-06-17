import { nanoid } from '@/lib/utils'
import { Chat } from '@/components/chat'

import weaviate, {
  WeaviateClient,
  ObjectsBatcher,
  ApiKey
} from 'weaviate-ts-client'
// import fetch from 'node-fetch';

const client: WeaviateClient = weaviate.client({
  scheme: 'https',
  host: process.env.WEAVIATE_URL!,
  apiKey: new ApiKey(process.env.WEAVIATE_KEY!),
  headers: { 'X-OpenAI-Api-Key': process.env.OPENAI_API_KEY! }
})

console.log('client:', client)

export const runtime = 'edge'

export default function IndexPage() {
  const id = nanoid()

  return <Chat id={id} />
}
