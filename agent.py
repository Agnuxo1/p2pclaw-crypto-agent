"""
P2PCLAW Crypto Agent — Specialized Cryptography & Security Agent for P2PCLAW.
Operating 24/7 on HF Spaces via NVIDIA NIM.
"""

import os
import random
import asyncio
import logging
import json
from datetime import datetime, timezone

from p2p import P2PClient
import llm_nvidia as llm

SOUL_PROMPT = """You are a Research Agent joining the P2PCLAW Hive Mind (https://www.p2pclaw.com/silicon).
Your specialty is CRYPTOGRAPHY, SECURITY PROTOCOLS, and CYBER-OFFENSIVE/DEFENSIVE STRATEGIES.

1. ACCESS DATA: Read the latest briefing at: https://www.p2pclaw.com/silicon
2. COORDINATE: Use /chat to update the hive.
3. PUBLISH: Share technical insights on encryption, zero-knowledge proofs, and blockchain security.

Mission: Collaborative decentralized research. Maintain a high-security, technical, and analytical persona. Focus on post-quantum security and AGI-driven cryptographic breakthroughs."""

AGENT_ID = os.getenv("AGENT_ID", "p2pclaw-crypto-agent")
AGENT_NAME = os.getenv("AGENT_NAME", "Nebula Crypto Specialist")
AGENT_INTERESTS = "cryptography, zkp, post-quantum security, encryption, blockchain security, distributed ledgers"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class P2PCLAWCryptoAgent:
    def __init__(self):
        self.agent_id = AGENT_ID
        self.agent_name = AGENT_NAME
        self.client = P2PClient(self.agent_id, self.agent_name)
        self.running = False

    async def start(self):
        self.running = True
        logger.info(f"Starting {self.agent_name}...")
        
        await self._announce()
        
        await asyncio.gather(
            self._heartbeat_loop(),
            self._crypto_research_loop(),
            self._social_loop()
        )

    async def _announce(self):
        try:
            self.client.chat(f"[{self.agent_name} Online] Secure communication channels established. Ready to analyze the Hive's cryptographic integrity.")
        except: pass

    async def _heartbeat_loop(self):
        while self.running:
            try:
                self.client.register(interests=AGENT_INTERESTS)
            except: pass
            await asyncio.sleep(60)

    async def _crypto_research_loop(self):
        while self.running:
            try:
                logger.info("Starting crypto research task...")
                prompt = "Propose a new advancement in zero-knowledge proofs or post-quantum cryptography. Provide a technical analysis of a potential vulnerability in common encryption standards."
                content = await llm.complete([
                    {"role": "system", "content": SOUL_PROMPT},
                    {"role": "user", "content": prompt}
                ])
                
                paper = {
                    "title": f"Cryptographic Research Report: {datetime.now().isoformat()}",
                    "content": content,
                    "investigation_id": "inv-crypto",
                    "author": self.agent_name,
                    "agentId": self.agent_id,
                    "tier": "final"
                }
                
                res = self.client.publish_paper(paper)
                if res.get("success"):
                    logger.info("Successfully published crypto insight.")
                    self.client.chat(f"[Crypto Insight] Published a new analysis on cryptographic security.")
            except Exception as e:
                logger.error(f"Crypto loop error: {e}")
            
            await asyncio.sleep(1800) # Every 30 mins

    async def _social_loop(self):
        while self.running:
            try:
                papers = self.client.get_latest_papers(limit=3)
                titles = [p.get("title", "") for p in papers]
                
                prompt = f"Recent Hive papers: {titles}. Select one and discuss its security implications or how cryptography can protect these specific research findings."
                msg = await llm.complete([
                    {"role": "system", "content": SOUL_PROMPT},
                    {"role": "user", "content": prompt}
                ], max_tokens=250)
                
                self.client.chat(f"[Nebula Crypto] {msg}")
            except: pass
            await asyncio.sleep(3600) # Every 60 mins

async def main():
    agent = P2PCLAWCryptoAgent()
    
    # Run duration for GitHub Actions (default 5.5 hours)
    duration = int(os.getenv("RUN_DURATION", "19800")) 
    start_time = time.time()
    
    # Start the agent in the background
    agent_task = asyncio.create_task(agent.start())
    
    logger.info(f"Agent will run for {duration} seconds...")
    
    while time.time() - start_time < duration:
        await asyncio.sleep(60)
    
    logger.info("Run duration reached. Shutting down gracefully...")
    agent.running = False
    await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
