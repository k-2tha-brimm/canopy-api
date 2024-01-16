"""The partition.py file defines the partition object, which is used for parsing
a partition name and returning the appropriate metadata filter.

To make things simple, the file only has one exported member, which is the 
`PartitionedDocument` class. This class is instantiated with a `partition_value: str` 
argument and the `content: str` argument. It is a superclass of the Canopy Document
object.
"""
from hashlib import sha3_256
from uuid import UUID
from typing import Dict, Optional

from canopy.models.data_models import Document, Query


class Partition:  # pylint: disable=too-few-public-methods
    """A partition object that can be used to get the metadata filter for a partition."""

    def __init__(self, partition_value: str):
        # Validate the partition value
        self.partition_value = partition_value

    def get_filter(self) -> str:
        """Get the filter that can be used to filter documents based on the partition value.

        Returns:
            str: The filter
        """
        metadata_filter = {}
        items = self.partition_value.split(":")
        for i, item in enumerate(items):
            match (i):
                # Extract the expert name
                case 0:
                    expert_name = item
                    metadata_filter["expert_name"] = expert_name
                case 1:
                    # Extract the document name
                    document_name = item
                    metadata_filter["document_name"] = document_name
                case _:
                    raise ValueError(
                        f"Partition value {self.partition_value} is invalid.\n"
                        f"It should be of the form `expert_name:document_name`."
                    )
        return metadata_filter


class PartitionedDocument(Document):  # pylint: disable=too-few-public-methods
    """A super class of the Canopy Document object to manually set metadata from
    the partition value.
    """

    def __init__(self, partition_name: str, content: str) -> None:
        metadata = Partition(partition_name).get_filter()

        # Set the seed for the UUID from the 8 byte keccak hash of the content str
        # This way if the same document is uploaded twice, we will not double store it

        super().__init__(id=self._get_uuid(content), text=content, metadata=metadata)

    @staticmethod
    def _get_uuid(content: str) -> str:
        """Get the UUID for the document.

        Args:
            content (str): The content of the document

        Returns:
            str: The UUID
        """
        # Convert the content to bytes
        content_bytes = content.encode("utf-8")

        # Get the keccak256 hash of the content
        hash_object = sha3_256(content_bytes)

        # Get the hash object in bytes
        hash_bytes = hash_object.digest()

        doc_id = UUID(bytes=hash_bytes[:16], version=4)

        return str(doc_id)


class PartitionedQuery(Query):
    """A query object that can be used to get query vectors for a partition."""

    def __init__(  # pylint: disable=unused-argument
        self,
        text: str,
        partition_name: str,
        metadata_filter: Optional[Dict] = None,
        **kwargs,
    ) -> None:
        # Establish the metadata_filter or setup a blank dictionary if none is provided
        metadata_filter = metadata_filter or {}

        # Update the metadata filter to include the partition filter values
        metadata_filter.update(Partition(partition_name).get_filter())
        print(metadata_filter)
        super().__init__(text=text, metadata_filter=metadata_filter, **kwargs)
